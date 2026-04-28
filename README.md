
# Capstone Project: Securing the Vroomi AI Assistant

Congratulations — you’ve made it to the final stretch of the course. This capstone is designed to help you cement what you’ve learned over the last several weeks by applying it to a realistic AI system case study.

In this project, you will step into the role of an AI Security Practitioner at Softmicro, the company behind the Vroomi AI assistant.

Softmicro is considering adding more agentic features to Vroomi, allowing it to take more autonomous actions such as making recommendations, drafting tickets, and interacting more directly with internal systems. Before moving forward, the CISO has asked for a security assessment.

Your role is to investigate the system, explore how it behaves under different attack and defense scenarios, and communicate your findings clearly.


## Project objective

The main goal of this capstone is communication, presentation, and consolidation of knowledge.

This is not intended to be a difficult open-ended engineering challenge. The tasks are therefore fairly scripted on purpose to help you focus on understanding what is happening, identifying key risks, and explaining those risks clearly.

There is no pass/fail, no grade, and no formal assessment. This capstone is purely for your own learning and development — so don’t stress about getting it “right”.


## How the capstone fits into the course

This capstone replaces the labs for:

Week 7
Week 8

You will spend these two weeks working through the project.

In Week 8, you have the option to present your findings — this could be:

- a short presentation
- a written summary
- or a walkthrough of your analysis

This is optional but highly encouraged, as it helps build real-world communication skills.


## How the capstone is structured

Each task is provided in a separate file, so you can choose the topics that interest you most.

You can complete as many or as few tasks as you like. The tasks do not need to be completed in order.

The only task that everyone should complete first is:

Task 0: Vroomi Baseline

This gives you the base system overview and helps you understand how Vroomi works before you explore attacks or defenses.


## Available tasks

Task 0: Vroomi Baseline
Explore the base Vroomi system and understand how user input, retrieval, the model, tools, and backend actions fit together.

Task 1: Prompt Injection
See how insecure handling of user input can lead to unsafe tool execution, then compare this with a defended version.

Task 2: System Prompt Leakage
Explore how internal instructions can be exposed through insecure application logic such as debug behaviour.

Task 3: Data Poisoning
See how false or manipulated information in a knowledge base can influence model behaviour and outputs.

Task 4: Sensitive Information Disclosure
Investigate how sensitive internal data can be exposed when the system includes it in model-accessible context.

Task 5: Misinformation
Explore how mixed-quality or misleading documents can cause the assistant to produce believable but incorrect answers.

Task 6: Improper Output Handling
See what happens when a system trusts model outputs too readily, especially when the model generates tool calls or structured instructions.


## What you should do

### 1. Start with Task 0

Everyone should begin with the Vroomi baseline so you have a shared understanding of the system before investigating any risks.

As you work through it, pay attention to:

- how Vroomi processes user input
- how it retrieves or uses information
- how it generates responses
- where it can take actions or make recommendations
- where trust boundaries exist
- where things could go wrong


### 2. Choose the tasks you want to explore

You do not need to complete every task. Choose whichever attack and defense scenarios you want to investigate.

For each task, focus on:

- what the system is doing
- what the risk is
- what changes in the defended version
- what this might mean in a real organisation


### 3. Create a system diagram

Draw a simple diagram of the Vroomi system. It does not need to be perfect — clarity matters more than complexity.

Your diagram might include:

- key components such as user input, retrieval, model, knowledge base, tools, and actions
- trust boundaries showing what is trusted vs untrusted
- annotations showing where threats are most likely to occur

A system diagram template has been provided to help you get started.


### 4. Record your findings

As you work, take note of the behaviours you observe and the main risks you identify.

A report template has also been provided to help you summarise your findings.

You are welcome to consider other risks that are not already included in the tasks in the report.


### 5. Prepare your recommendation

Your final task is to communicate your findings clearly, as though you were presenting them to the CISO or another decision-maker.

Your recommendation might consider:

- the main risks in the current system
- which risks seem most serious
- whether the defences appear effective
- whether the system seems ready for more agentic features
- what safeguards should be added first

You may conclude with a:

Go, No-Go, or Conditional Go with safeguards


## How to approach this project

Think of this less as a coding task and more as an investigation.

You are:

- testing assumptions
- identifying weaknesses
- comparing attack and defense behaviour
- explaining risk clearly
- practising how to communicate AI - security issues to others

There is no single correct answer. What matters most is that you understand what you are seeing and can explain it in a clear, structured way.


## Final note

This capstone is not graded, there is no pass or fail, and there is no formal assessment attached to it. It is designed purely to help you build confidence and consolidate your understanding — so take the pressure off yourself.

Instead, think of this as something you can showcase:

- you can include your findings in a portfolio
- upload your work to GitHub
- or share it with prospective employers

Being able to clearly explain how AI systems fail — and how to secure them — is a valuable real-world skill.

Take your time, explore the tasks that interest you, and use this as an opportunity to build something you’re proud to share.