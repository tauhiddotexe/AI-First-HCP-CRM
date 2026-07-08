import { createSlice } from '@reduxjs/toolkit'

interface AgentState {
  currentIntent: string | null
  lastToolUsed: string | null
  lastResponse: string | null
}

const initialState: AgentState = {
  currentIntent: null,
  lastToolUsed: null,
  lastResponse: null,
}

const agentSlice = createSlice({
  name: 'agent',
  initialState,
  reducers: {
    setAgentIntent(state, action) {
      state.currentIntent = action.payload
    },
    setLastToolUsed(state, action) {
      state.lastToolUsed = action.payload
    },
    setLastResponse(state, action) {
      state.lastResponse = action.payload
    },
  },
})

export const { setAgentIntent, setLastToolUsed, setLastResponse } = agentSlice.actions
export default agentSlice.reducer
