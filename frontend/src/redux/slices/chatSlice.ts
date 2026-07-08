import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { agentApi } from '@/services/api'
import type { ChatMessage, AgentChatResponse } from '@/types'

interface ChatState {
  messages: ChatMessage[]
  isProcessing: boolean
  currentTool: string | null
  lastResponse: AgentChatResponse | null
  error: string | null
}

const initialState: ChatState = {
  messages: [],
  isProcessing: false,
  currentTool: null,
  lastResponse: null,
  error: null,
}

export const sendMessage = createAsyncThunk<
  AgentChatResponse,
  { message: string; interaction_id?: string | null }
>('chat/sendMessage', async (payload) => {
  const response = await agentApi.chat(payload)
  return response.data
})

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage(state, action) {
      state.messages.push(action.payload)
    },
    clearChat(state) {
      state.messages = []
      state.error = null
      state.lastResponse = null
    },
    clearLastResponse(state) {
      state.lastResponse = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.isProcessing = true
        state.error = null
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.isProcessing = false
        state.currentTool = action.payload.tool_used
        state.lastResponse = action.payload
        state.messages.push({
          id: crypto.randomUUID(),
          role: 'assistant',
          message: action.payload.assistant_message,
          tool_used: action.payload.tool_used,
          created_at: new Date().toISOString(),
        })
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.isProcessing = false
        state.error = action.error.message || 'Failed to process message'
      })
  },
})

export const { addMessage, clearChat, clearLastResponse } = chatSlice.actions
export default chatSlice.reducer
