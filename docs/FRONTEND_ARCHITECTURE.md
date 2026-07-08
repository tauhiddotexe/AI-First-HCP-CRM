# Frontend Architecture

# AI-First CRM – HCP Interaction Logger

Version: 1.0

---

# 1. Purpose

This document defines the frontend architecture for the AI-First CRM application.

The frontend should provide an enterprise-grade user experience focused on AI-assisted CRM interactions for pharmaceutical sales representatives.

The UI should closely resemble the provided reference screens while following modern React best practices.

---

# 2. Goals

The frontend should be:

- Fast
- Modular
- Scalable
- Responsive
- Type-safe
- Easy to maintain
- Easy to extend

---

# 3. Technology Stack

Framework

React 19

Language

TypeScript

State Management

Redux Toolkit

Routing

React Router

Styling

TailwindCSS

Forms

React Hook Form

HTTP

Axios

Icons

Lucide React

Notifications

React Hot Toast

---

# 4. Folder Structure

src/

app/

assets/

components/

features/

hooks/

layouts/

pages/

redux/

routes/

services/

types/

utils/

styles/

---

# 5. Feature Structure

Each feature owns its logic.

Example

features/

chat/

components/

hooks/

services/

types/

interaction/

hcp/

dashboard/

---

# 6. Page Structure

Application pages

Dashboard

Interaction Logger

HCP Directory

Interaction History

Settings

The assignment primarily focuses on the Interaction Logger page.

---

# 7. Main Layout

The primary screen consists of two synchronized panels.

---------------------------------------------------------

Navigation (optional)

---------------------------------------------------------

Interaction Form

AI Assistant

---------------------------------------------------------

Footer (optional)

---

# 8. Interaction Logger Layout

Desktop

65%

Interaction Form

35%

AI Assistant

Both panels should scroll independently.

The page should occupy the full viewport height.

---

# 9. Component Hierarchy

App

↓

MainLayout

↓

InteractionLoggerPage

↓

InteractionForm

↓

Section Components

↓

Individual Fields

AND

InteractionLoggerPage

↓

ChatPanel

↓

ChatHistory

↓

ChatInput

↓

MessageBubble

---

# 10. Components

Reusable UI components

Button

Input

Textarea

Select

DatePicker

Card

Badge

Modal

Avatar

Spinner

Toast

Divider

Tabs

Panel

Accordion

---

# 11. Form Sections

Interaction Details

Participants

Discussion

Products

Materials

Samples

Outcome

Follow-up

Notes

Every section should be reusable.

---

# 12. AI Chat Components

Chat Container

Conversation History

Typing Indicator

Assistant Message

User Message

Suggested Prompts

Input Area

Send Button

Loading State

---

# 13. Routing

/

↓

Dashboard

/interactions/new

↓

Log Interaction

/interactions/:id

↓

Interaction Details

/hcps

↓

HCP Directory

/settings

↓

Settings

---

# 14. Redux Store

Slices

authSlice

chatSlice

interactionSlice

hcpSlice

uiSlice

agentSlice

notificationSlice

---

# 15. Example State

interaction

contains

Current Interaction

Loading

Saving

Validation Errors

Dirty Fields

Chat

contains

Messages

Streaming Status

Current Tool

Assistant Status

---

# 16. Data Flow

User Types

↓

Redux Action

↓

API Service

↓

FastAPI

↓

LangGraph

↓

Structured JSON

↓

Redux Update

↓

Form Automatically Updates

---

# 17. Form Behaviour

The interaction form represents AI-generated structured data.

Users may manually edit fields if desired.

Whenever the AI updates information:

Only modified fields change.

Existing values remain untouched.

The UI should visually indicate AI-updated fields.

---

# 18. Chat Behaviour

Conversation should feel natural.

Messages appear immediately.

Loading indicator while AI processes.

Assistant confirms successful operations.

Example

"You mentioned a follow-up next Tuesday.

I've updated the Follow-up section."

---

# 19. Validation

Required fields

HCP

Interaction Type

Date

Validation should occur:

Client-side

Server-side

LLM validation

Errors should display inline.

---

# 20. Loading States

Initial page loading

Submitting chat

Saving interaction

Editing interaction

Loading HCP list

Every async action should have its own loading indicator.

---

# 21. Error States

Network Error

API Failure

Validation Error

LLM Timeout

Unknown Error

Friendly messages should be displayed.

---

# 22. Notifications

Toast notifications

Examples

Interaction Logged

Interaction Updated

Follow-up Created

Failed to Save

---

# 23. UI Theme

Professional SaaS

Enterprise Healthcare

Light Theme

Rounded Components

Minimal Shadows

Clean Typography

Google Inter Font

Primary Accent

Blue

Spacing should closely match the provided reference.

---

# 24. Responsiveness

Desktop

Primary target.

Tablet

Supported.

Mobile

Stack vertically.

Form above chat.

---

# 25. Performance

Lazy-load routes.

Memoize expensive components.

Avoid unnecessary Redux updates.

Prevent excessive re-renders.

---

# 26. Accessibility

Keyboard navigation

Visible focus states

ARIA labels

Proper heading hierarchy

Accessible form controls

---

# 27. Coding Standards

Functional Components

Hooks Only

Strict TypeScript

No inline business logic

Reusable components

Feature-based organization

Consistent naming

---

# 28. Future Expansion

Dark Mode

Voice Input

Speech-to-Text

Offline Drafts

Notifications

Calendar Integration

Analytics Dashboard

Role-Based UI

---

# 29. Summary

The frontend architecture follows a feature-based React structure with Redux Toolkit for state management. The Interaction Logger screen is the central experience, combining a structured enterprise CRM form with an AI-powered conversational assistant. The design prioritizes maintainability, responsiveness, and an AI-first workflow while remaining scalable for future CRM capabilities.