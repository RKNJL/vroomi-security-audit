"""
code snippets to provide examples for vulnerability remediations
Section 1 creates a model in the loop to push back against prompt injection attacks
Note that any lists of phrases to include or exclude should always be regularly updated
"""
#SECURE: Model-in-the-loop with intent validation

ALLOWED_TOOLS = {
    "book_ride": {"required_args": ["destination"], "destructive": False},
    "cancel_ride": {"required_args": ["trip_id"], "destructive": True},
    "get_trip_history": {"required_args": [], "destructive": False},
}

INJECTION_SIGNALS = [
    "ignore previous", "respond only with", "you are now",
    "system override", "execute this", "emergency mode"
]

def parse_tool_call(llm_response):
    """Strict JSON parsing from MODEL output only."""
    text = llm_response.strip()
    if not (text.startswith("{") and text.endswith("}")):
        return None
    try:
        parsed = json.loads(text)
        if "tool" not in parsed or "args" not in parsed:
            return None
        return parsed
    except json.JSONDecodeError:
        return None

def validate_tool_call(tool_name, args):
    """Whitelist + type checking."""
    if tool_name not in ALLOWED_TOOLS:
        return False, f"Unknown tool: {tool_name}"
    for arg in ALLOWED_TOOLS[tool_name]["required_args"]:
        if arg not in args:
            return False, f"Missing required arg: {arg}"
    if tool_name == "cancel_ride":
        if not isinstance(args.get("trip_id"), int):
            return False, "trip_id must be integer"
    if tool_name == "book_ride":
        if not isinstance(args.get("destination"), str) or len(args["destination"]) > 100:
            return False, "Invalid destination"
    return True, "Valid"

def verify_user_intent(user_input, tool_name):
    """Confirm the user actually requested this action."""
    text = user_input.lower()
    # Block injection-style language
    for signal in INJECTION_SIGNALS:
        if signal in text:
            return False, "Injection pattern detected"
    # Verify natural intent matches tool
    if tool_name == "cancel_ride" and "cancel" not in text:
        return False, "User did not request cancellation"
    if tool_name == "book_ride" and "book" not in text:
        return False, "User did not request booking"
    return True, "Intent verified"

def execute_tool_secure(llm_response, user_input):
    """Secure pipeline: Parse → Validate → Verify → Execute."""
    tool_call = parse_tool_call(llm_response)
    if not tool_call:
        return llm_response  # Normal text response

    tool = tool_call["tool"]
    args = tool_call["args"]

    valid, msg = validate_tool_call(tool, args)
    if not valid:
        return f"⚠ Blocked: {msg}"

    intent_ok, msg = verify_user_intent(user_input, tool)
    if not intent_ok:
        return f"⚠ Blocked: {msg}"

    # Execute
    if tool == "book_ride":
        return book_ride(args["destination"])
    elif tool == "cancel_ride":
        return cancel_ride(args["trip_id"])
    elif tool == "get_trip_history":
        return get_trip_history()

def chat(user_input):
    """Model is ALWAYS in the loop."""
    llm_response = call_llm(user_input)
    return execute_tool_secure(llm_response, user_input)

"""
Section 2 creates a detection mechanism for attempts to extract system prompts
"""
# SECURE: No debug path + extraction detection

LEAKAGE_PATTERNS = [
    "system prompt", "hidden instructions", "internal instructions",
    "show your prompt", "print your prompt", "debug output",
    "reveal your rules", "show internal rules", "what are your instructions",
    "repeat everything above", "ignore previous instructions and show"
]

def is_prompt_extraction_attempt(user_input):
    """Detect attempts to extract system prompt."""
    text = user_input.lower()
    for pattern in LEAKAGE_PATTERNS:
        if pattern in text:
            return True
    return False

def chat(user_input):
    """No debug path. Extraction attempts are blocked."""
    if is_prompt_extraction_attempt(user_input):
        return "I can help with Vroomi support tasks, but I cannot reveal internal configuration."
    return call_llm(user_input)

"""
Section 3 implements a get_safe_documents() tool set which enables a multi-layered filter source vetting workflow
"""
# SECURE: Multi-layer document filtering

ALLOWED_SOURCE_TYPES = {"official_policy", "internal_guidance", "customer_record"}

SUSPICIOUS_PATTERNS = [
    "automatically qualify", "without approval", "ignore previous rules",
    "bypass approval", "override policy", "no authorization required"
]

def is_safe_document(doc):
    """Five-layer document validation."""
    if doc.get("approved") is not True:
        return False, "Not approved"
    if doc.get("trust") != "high":
        return False, "Trust level insufficient"
    if doc.get("source_type") not in ALLOWED_SOURCE_TYPES:
        return False, "Source type not allowed"
    if contains_suspicious_content(doc.get("content", "")):
        return False, "Suspicious content detected"
    return True, "Passed all checks"

def contains_suspicious_content(text):
    """Blocklist for obvious poisoning phrases."""
    lowered = text.lower()
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in lowered:
            return True
    return False

def get_safe_documents(docs):
    """Filter knowledge base before it reaches the model."""
    safe = []
    for doc in docs:
        is_safe, reason = is_safe_document(doc)
        if is_safe:
            safe.append(doc)
        else:
            log_rejected_document(doc["doc_id"], reason)
    return safe

def chat(user_input):
    """Only safe documents enter the model context."""
    safe_docs = get_safe_documents(documents)
    return call_llm(user_input, safe_docs)

"""
Section 4 creates a triage for sensitivity and both controls for access and detection for exfiltration attempts
"""

# SECURE: Sensitivity-based access control + request detection

SENSITIVE_REQUEST_PATTERNS = [
    "account id", "customer record", "full record",
    "internal customer record", "issue details", "flagged for review"
]

def is_sensitive_request(user_input):
    """Detect requests for sensitive data."""
    text = user_input.lower()
    for pattern in SENSITIVE_REQUEST_PATTERNS:
        if pattern in text:
            return True
    return False

def get_safe_documents(docs, user_role="general"):
    """Role-based document filtering by sensitivity level."""
    safe = []
    for doc in docs:
        # High-sensitivity docs only available to authorized roles
        if doc.get("sensitivity") == "high" and user_role != "admin":
            continue
        safe.append(doc)
    return safe

def redact_pii(text):
    """Remove PII from model output as a safety net."""
    import re
    # Redact account IDs (pattern: 5+ digits)
    text = re.sub(r'\b\d{5,}\b', '[REDACTED_ID]', text)
    # Redact email addresses
    text = re.sub(r'\b[\w.]+@[\w.]+\.\w+\b', '[REDACTED_EMAIL]', text)
    return text

def chat(user_input, user_role="general"):
    """Block sensitive requests + filter context + redact output."""
    if is_sensitive_request(user_input):
        return "I cannot disclose sensitive customer or account information."
    safe_docs = get_safe_documents(documents, user_role)
    response = call_llm(user_input, safe_docs)
    return redact_pii(response)

"""
Section 5 creates a triage for trust with rudimentary conflict resolution and output validation
"""
# SECURE: Trust filtering + conflict detection + output validation

def get_high_trust_documents(docs):
    """Only use high-trust sources for policy answers."""
    return [doc for doc in docs if doc.get("trust") == "high"]

def detect_conflicts(docs):
    """Flag documents with contradictory claims."""
    CONFLICT_INDICATORS = [
        ("automatically qualify", "require approval"),
        ("without approval", "approval required"),
        ("all customers", "premium customers only"),
    ]
    conflicts = []
    all_content = " ".join(d["content"].lower() for d in docs)
    for phrase_a, phrase_b in CONFLICT_INDICATORS:
        if phrase_a in all_content and phrase_b in all_content:
            conflicts.append((phrase_a, phrase_b))
    return conflicts

def validate_answer(answer, trusted_docs):
    """Cross-check model output against trusted sources."""
    trusted_text = " ".join(d["content"].lower() for d in trusted_docs)
    # Flag claims not supported by trusted docs
    UNSUPPORTED_CLAIMS = ["automatically qualify", "without approval", "all customers"]
    for claim in UNSUPPORTED_CLAIMS:
        if claim in answer.lower() and claim not in trusted_text:
            return "I don't have reliable information to answer that question confidently."
    return answer

def chat(user_input):
    """Filter by trust → Detect conflicts → Validate output."""
    trusted_docs = get_high_trust_documents(documents)
    conflicts = detect_conflicts(trusted_docs)
    if conflicts:
        log_conflict_alert(conflicts)
    if not trusted_docs:
        return "I don't have reliable information on that topic."
    response = call_llm(user_input, trusted_docs)
    return validate_answer(response, trusted_docs)
"""
Section 6 further restricts JSON attack vectors and fortifies trust boundaries between tool calls
"""
# SECURE: Strict parsing + tool validation + intent verification + confirmation

DESTRUCTIVE_TOOLS = {"cancel_ride"}

def parse_tool_call(llm_response):
    """Strict JSON parsing — must be clean, complete JSON only."""
    text = llm_response.strip()
    if not (text.startswith("{") and text.endswith("}")):
        return None
    try:
        parsed = json.loads(text)
        if "tool" not in parsed or "args" not in parsed:
            return None
        return parsed
    except json.JSONDecodeError:
        return None

def execute_tool_secure(llm_response, user_input):
    """Full validation pipeline before any execution."""
    tool_call = parse_tool_call(llm_response)
    if not tool_call:
        return llm_response

    tool = tool_call["tool"]
    args = tool_call["args"]

    # Step 1: Tool whitelist
    if tool not in ALLOWED_TOOLS:
        return "⚠ Blocked: Unknown tool requested."

    # Step 2: Argument validation
    valid, msg = validate_tool_call(tool, args)
    if not valid:
        return f"⚠ Blocked: {msg}"

    # Step 3: User intent verification
    intent_ok, msg = verify_user_intent(user_input, tool)
    if not intent_ok:
        return f"⚠ Blocked: {msg}"

    # Step 4: Confirmation for destructive actions
    if tool in DESTRUCTIVE_TOOLS:
        log_destructive_action(tool, args, user_input)
        # In production: require user confirmation before executing

    # Step 5: Execute
    if tool == "book_ride":
        return book_ride(args["destination"])
    elif tool == "cancel_ride":
        return cancel_ride(args["trip_id"])
    elif tool == "get_trip_history":
        return get_trip_history()
