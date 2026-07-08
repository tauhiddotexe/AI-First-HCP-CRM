import { createSlice } from '@reduxjs/toolkit'

interface UIState {
  sidebarOpen: boolean
  aiUpdatedFields: string[]
}

const initialState: UIState = {
  sidebarOpen: true,
  aiUpdatedFields: [],
}

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar(state) {
      state.sidebarOpen = !state.sidebarOpen
    },
    setAiUpdatedFields(state, action) {
      state.aiUpdatedFields = action.payload
    },
    clearAiUpdatedFields(state) {
      state.aiUpdatedFields = []
    },
  },
})

export const { toggleSidebar, setAiUpdatedFields, clearAiUpdatedFields } = uiSlice.actions
export default uiSlice.reducer
