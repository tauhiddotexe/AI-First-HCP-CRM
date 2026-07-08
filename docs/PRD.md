# Product Requirements Document (PRD)

# AI-First CRM – HCP Interaction Logger

Version: 1.0

---

# 1. Overview

## Project Name

AI-First CRM – HCP Module

## Goal

Build an AI-first Customer Relationship Management (CRM) module for Healthcare Professional (HCP) interactions.

Unlike traditional CRMs where users manually complete forms, this application should treat the AI assistant as the primary interface.

Users should naturally describe their interaction with an HCP using conversational language.

The LangGraph agent must interpret the conversation, decide which tool(s) to execute, extract structured information using an LLM, and automatically populate the interaction form.

The left-side form should primarily represent AI-generated structured data rather than manual user input.

This application should resemble an enterprise Life Sciences CRM designed for pharmaceutical sales representatives.

---

# 2. Assignment Requirements

The project MUST satisfy all assignment requirements.

Required technologies:

- React
- Redux Toolkit
- FastAPI
- LangGraph
- Groq API
- gemma2-9b-it
- PostgreSQL (preferred) or MySQL
- Google Inter font

No hardcoded parsing logic may replace the LangGraph + LLM pipeline.

The AI must be responsible for understanding natural language.

---

# 3. Product Vision

Sales representatives frequently visit doctors, hospitals, and healthcare professionals.

After every meeting they must document:

- who they met
- discussion topics
- products discussed
- objections
- sentiment
- follow-up actions
- samples shared
- materials distributed

Traditional CRMs require lengthy manual forms.

This project reduces documentation time by allowing the representative to simply describe the meeting naturally.

The AI performs the remaining work.

---

# 4. Target Users

Primary User

Pharmaceutical Sales Representative

Responsibilities

- Visit HCPs
- Promote products
- Record meeting notes
- Plan follow-ups
- Track relationships

Secondary User

Sales Manager

Responsibilities

- Review interactions
- Track field activity
- Analyze engagement quality

---

# 5. Core Experience

The application consists of two synchronized panels.

Left Panel

Enterprise interaction form

Right Panel

AI assistant

The user should primarily interact through chat.

The AI continuously updates the form.

Users should feel like they are talking to an intelligent assistant rather than filling out CRM fields.

---

# 6. Reference UI

The supplied reference screenshots should be treated as the primary UI reference.

The implementation should closely resemble:

- layout
- spacing
- component hierarchy
- scrolling behavior
- interaction flow

Pixel-perfect replication is not required.

However the UX should closely match.

---

# 7. Layout

Split screen

Approximately

65% Form

35% AI Assistant

Desktop first.

Entire page height.

Independent scrolling.

---

# 8. Left Panel

Title

Log HCP Interaction

Contains a long enterprise form.

Representative sections include

Interaction Details

- HCP
- Interaction Type
- Date
- Time

Participants

- Attendees

Discussion

- Topics Discussed

Materials

- Materials Shared
- Samples Distributed

Assessment

- Sentiment
- Outcomes

Planning

- Follow-up Actions

Additional Notes

Future fields can be added without changing architecture.

---

# 9. Right Panel

AI Assistant

Chat interface.

Contains

Conversation history

Input box

Submit button

Loading indicator

Streaming response (optional)

Suggested prompts

Example prompt

"Today I met Dr. Smith and discussed Product X. He was interested but concerned about pricing. I shared brochures and scheduled a follow-up next Tuesday."

---

# 10. Interaction Flow

User enters natural language.

↓

Frontend sends request.

↓

FastAPI.

↓

LangGraph.

↓

Planner.

↓

Tool Selection.

↓

LLM.

↓

Structured extraction.

↓

Validation.

↓

Database.

↓

Redux update.

↓

Form automatically updates.

↓

AI confirms extracted information.

---

# 11. Manual Editing

The assignment allows a structured form.

However AI remains the primary interface.

Preferred behavior

Users edit by chatting.

Example

"The meeting was actually yesterday."

The Edit Interaction Tool updates only the Date field.

Other fields remain unchanged.

---

# 12. AI Responsibilities

The AI should understand

Doctor names

Dates

Relative dates

Products

Medicines

Hospitals

Materials

Sentiment

Follow-up actions

Meeting outcomes

Discussion topics

It should normalize extracted values into structured CRM data.

---

# 13. LangGraph Agent

The LangGraph agent orchestrates all CRM intelligence.

Responsibilities

Intent detection

Entity extraction

Validation

Tool routing

Database interaction

Response generation

Conversation memory

---

# 14. Required LangGraph Tools

Minimum five tools.

## Tool 1

Log Interaction

Purpose

Create structured CRM interaction.

Input

Natural language.

Output

Structured interaction.

Responsibilities

Extract

Doctor

Date

Time

Topics

Sentiment

Materials

Summary

Persist database.

---

## Tool 2

Edit Interaction

Purpose

Modify existing interaction.

Must only update requested fields.

Other fields remain unchanged.

---

## Tool 3

Retrieve Interaction History

Purpose

Retrieve previous meetings.

Summarize previous interactions.

---

## Tool 4

Suggest Next Best Action

Purpose

Recommend follow-up.

Examples

Schedule visit

Share samples

Provide literature

Arrange product demo

Medical education session

---

## Tool 5

Generate Visit Summary

Purpose

Generate concise CRM summary.

Useful for managers.

---

# 15. Redux State

Suggested slices

auth

chat

interactionForm

hcp

agent

ui

loading

errors

---

# 16. Database

Core tables

hcp

interactions

interaction_materials

interaction_samples

chat_messages

users

future extensibility should be considered.

---

# 17. API Endpoints

POST /agent/chat

POST /interactions

PATCH /interactions/{id}

GET /interactions/{id}

GET /hcps

GET /interactions/history

---

# 18. Validation

Required

HCP

Interaction Type

Date

Optional

Materials

Topics

Summary

Sentiment

AI should infer missing information when reasonable.

Otherwise ask follow-up questions.

---

# 19. Error Handling

Examples

Unknown doctor

Invalid date

Incomplete interaction

LLM timeout

Database failure

Network error

Gracefully notify user.

---

# 20. Non Functional Requirements

Responsive

Accessible

Fast

Reusable components

Clean architecture

Typed APIs

Modular services

Scalable folder structure

---

# 21. UI Guidelines

Font

Inter

Style

Enterprise SaaS

Clean

Minimal

Professional

Rounded inputs

Light theme

Subtle shadows

Blue accent colors

High information density

---

# 22. Folder Structure

Frontend

components

pages

features

redux

hooks

services

types

utils

Backend

api

agents

graph

tools

models

schemas

database

services

prompts

core

---

# 23. Acceptance Criteria

✓ Split screen interface

✓ AI assistant functional

✓ LangGraph integrated

✓ Groq LLM integrated

✓ Five LangGraph tools implemented

✓ Form auto-populates

✓ Edit tool preserves unchanged fields

✓ Redux manages application state

✓ FastAPI backend operational

✓ PostgreSQL integration

✓ Professional enterprise UI

✓ README included

✓ Project ready for demonstration