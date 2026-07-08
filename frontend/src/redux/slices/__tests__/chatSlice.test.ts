import chatReducer, { addMessage, clearChat, clearLastResponse } from '../chatSlice'
import type { ChatMessage, AgentChatResponse } from '@/types'

const mockMessage: ChatMessage = {
  id: '1',
  role: 'user',
  message: 'Hello',
  created_at: '2024-01-01T00:00:00Z',
}

const mockAssistantMessage: ChatMessage = {
  id: '2',
  role: 'assistant',
  message: 'Hi there',
  created_at: '2024-01-01T00:00:01Z',
}

describe('chatSlice', () => {
  const initialState = {
    messages: [],
    isProcessing: false,
    currentTool: null,
    lastResponse: null,
    error: null,
  }

  it('returns initial state', () => {
    const state = chatReducer(undefined, { type: 'unknown' })
    expect(state).toEqual(initialState)
  })

  it('adds a message', () => {
    const state = chatReducer(initialState, addMessage(mockMessage))
    expect(state.messages).toHaveLength(1)
    expect(state.messages[0]).toEqual(mockMessage)
  })

  it('adds multiple messages', () => {
    const state = [mockMessage, mockAssistantMessage].reduce(
      (s, msg) => chatReducer(s, addMessage(msg)),
      initialState,
    )
    expect(state.messages).toHaveLength(2)
  })

  it('clears chat', () => {
    const stateWithMessages = chatReducer(initialState, addMessage(mockMessage))
    const state = chatReducer(stateWithMessages, clearChat())
    expect(state.messages).toHaveLength(0)
    expect(state.lastResponse).toBeNull()
    expect(state.error).toBeNull()
  })

  it('clears last response', () => {
    const stateWithResponse = chatReducer(initialState, {
      type: 'chat/sendMessage/fulfilled',
      payload: {
        assistant_message: 'Ok',
        tool_used: 'log_interaction',
        updated_form: {},
        interaction_id: '123',
      } satisfies AgentChatResponse,
    })
    expect(stateWithResponse.lastResponse).not.toBeNull()
    const state = chatReducer(stateWithResponse, clearLastResponse())
    expect(state.lastResponse).toBeNull()
  })

  it('sets processing on pending', () => {
    const state = chatReducer(initialState, {
      type: 'chat/sendMessage/pending',
    })
    expect(state.isProcessing).toBe(true)
    expect(state.error).toBeNull()
  })

  it('handles fulfilled', () => {
    const response: AgentChatResponse = {
      assistant_message: 'Logged interaction with Dr. Smith',
      tool_used: 'log_interaction',
      updated_form: { interaction_type: 'Face-to-Face', sentiment: 'positive' },
      interaction_id: 'int-123',
    }
    const state = chatReducer(
      { ...initialState, isProcessing: true },
      {
        type: 'chat/sendMessage/fulfilled',
        payload: response,
      },
    )
    expect(state.isProcessing).toBe(false)
    expect(state.currentTool).toBe('log_interaction')
    expect(state.lastResponse).toEqual(response)
    expect(state.messages).toHaveLength(1)
    expect(state.messages[0]!.role).toBe('assistant')
    expect(state.messages[0]!.message).toBe('Logged interaction with Dr. Smith')
  })

  it('handles rejected', () => {
    const state = chatReducer(
      { ...initialState, isProcessing: true },
      {
        type: 'chat/sendMessage/rejected',
        error: { message: 'Network error' },
      },
    )
    expect(state.isProcessing).toBe(false)
    expect(state.error).toBe('Network error')
  })
})
