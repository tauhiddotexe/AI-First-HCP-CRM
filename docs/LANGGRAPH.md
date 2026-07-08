# LangGraph Architecture

# AI-First CRM – HCP Interaction Logger

Version: 1.0

---

# 1. Purpose

This document defines the architecture of the LangGraph-powered AI agent responsible for understanding user conversations, selecting the appropriate CRM tool, extracting structured information, validating results, and generating intelligent responses.

Unlike a traditional chatbot, the LangGraph agent is the orchestration engine of the CRM. It transforms natural language into structured CRM records and manages the interaction lifecycle.

---

# 2. Responsibilities

The LangGraph agent is responsible for:

- Understanding user intent
- Maintaining conversation context
- Selecting the correct tool
- Extracting structured CRM data
- Validating extracted entities
- Persisting interaction data
- Editing existing records
- Retrieving historical interactions
- Suggesting next best actions
- Generating concise summaries

The agent should never directly manipulate the database. All persistence must happen through tools.

---

# 3. High-Level Workflow

User Message
        │
        ▼
Conversation State
        │
        ▼
Intent Detection
        │
        ▼
Planner Node
        │
        ▼
Tool Selection
        │
        ▼
Execute Tool
        │
        ▼
Validate Result
        │
        ▼
Generate Assistant Response
        │
        ▼
Return Updated State

---

# 4. Graph State

The shared state passed between nodes should contain:

```python
{
    "messages": [],
    "user_input": "",
    "intent": "",
    "selected_tool": "",
    "entities": {},
    "interaction": {},
    "tool_result": {},
    "assistant_response": "",
    "errors": [],
    "metadata": {}
}
```

State should be immutable where practical, with each node returning only the fields it updates.

---

# 5. Graph Nodes

## Start Node

Receives user request.

Responsibilities:

- Initialize state
- Store latest message

---

## Intent Detection Node

Determine the user's objective.

Supported intents:

- Log interaction
- Edit interaction
- Retrieve interaction
- Generate summary
- Recommend next action
- General conversation

Output:

```text
Intent
Confidence
```

---

## Planner Node

Converts user intent into an execution plan.

Example:

User:

"I met Dr Shah today."

Execution:

Intent

↓

Log Interaction

↓

Extract Entities

↓

Validate

↓

Save

↓

Respond

---

## Tool Router

Maps intent to tools.

Example

Log Interaction

↓

LogInteractionTool

Edit

↓

EditInteractionTool

History

↓

RetrieveHistoryTool

Summary

↓

VisitSummaryTool

Recommendation

↓

NextBestActionTool

---

## Validation Node

Ensures extracted information is usable.

Checks:

Required fields

Date formats

Unknown HCP

Empty summaries

Invalid interaction type

If validation fails:

Ask follow-up questions.

---

## Response Generator

Creates natural responses.

Example:

"I've successfully logged today's meeting with Dr. Shah.

I extracted:

• Product discussed

• Pricing concern

• Positive engagement

• Follow-up scheduled next Tuesday."

---

# 6. Tool Definitions

---

## Tool 1

### Log Interaction

Purpose

Create a new CRM interaction.

Input

Natural language conversation.

Responsibilities

- Extract entities
- Generate structured interaction
- Produce AI summary
- Store interaction

Output

```json
{
  "interaction_id": "...",
  "status": "success"
}
```

---

## Tool 2

### Edit Interaction

Purpose

Modify an existing interaction.

Responsibilities

- Identify target record
- Update requested fields only
- Preserve all other values
- Record update timestamp

---

## Tool 3

### Retrieve Interaction History

Purpose

Fetch previous HCP interactions.

Responsibilities

- Retrieve records
- Order chronologically
- Generate concise summary

Example

"You last met Dr. Shah 12 days ago.

Topics discussed:

• Product X

• Safety profile

Follow-up was pending."

---

## Tool 4

### Suggest Next Best Action

Purpose

Recommend future engagement.

Example outputs

- Schedule follow-up
- Share literature
- Arrange product demo
- Send efficacy data
- Invite to webinar

Recommendations should consider previous interaction history.

---

## Tool 5

### Generate Visit Summary

Purpose

Generate manager-friendly notes.

Example

"Representative met Dr. Shah to discuss Product X.

The physician expressed positive interest but requested additional efficacy evidence.

Follow-up planned for next week."

---

# 7. Entity Extraction

The LLM should identify:

Doctor Name

Hospital

Clinic

Interaction Type

Date

Time

Products

Medicines

Competitors

Discussion Topics

Objections

Materials Shared

Samples Distributed

Sentiment

Follow-up

Meeting Outcome

Notes

Unknown entities should remain null rather than hallucinated.

---

# 8. Prompting Strategy

System Prompt

Defines assistant role.

Developer Prompt

Defines extraction rules.

User Prompt

Contains conversation.

Prompt template should instruct the LLM to always produce structured JSON matching the CRM schema.

---

# 9. Memory Strategy

Conversation memory should include:

Current interaction

Recent messages

Latest extracted entities

Pending clarifications

Previously logged interaction ID

Only the minimum required context should be passed to reduce token usage.

---

# 10. Decision Logic

Example

User:

"I met Dr Patel yesterday."

↓

Intent

Log Interaction

↓

Missing fields?

↓

Yes

↓

Ask question

"What products were discussed?"

↓

Receive answer

↓

Continue extraction

↓

Save interaction

---

# 11. Error Handling

Possible failures

LLM timeout

Malformed JSON

Missing fields

Unknown HCP

Database error

Tool exception

Each failure should return a user-friendly explanation and preserve conversation state.

---

# 12. Extensibility

Future tools may include:

Schedule Follow-up

Generate Email

Create Calendar Event

Recommend Marketing Material

Doctor Insights

Analytics

Medical Information Lookup

Voice Transcription

The graph should support adding new tools without modifying existing nodes.

---

# 13. Design Principles

- One responsibility per node
- Tools perform business actions
- Nodes orchestrate workflow
- State remains explicit
- LLM generates structured output
- Validation occurs before persistence
- Database access only through tools
- Easily testable and extensible

---

# 14. End-to-End Example

User:

"I met Dr. Shah today. We discussed Product A. He was interested but asked about long-term safety. I shared a brochure and scheduled a follow-up next Tuesday."

↓

Intent Detection

↓

Planner

↓

Log Interaction Tool

↓

LLM Entity Extraction

↓

Validation

↓

Persist to Database

↓

Generate Visit Summary

↓

Return Success Response

↓

Redux Updates Form Automatically

---

# 15. Summary

The LangGraph agent is the intelligence layer of the application. It interprets user conversations, coordinates specialized tools, validates extracted information, and maintains conversation context. By separating orchestration from tool execution, the design remains modular, scalable, and easy to extend with future AI capabilities.