import { createSlice } from '@reduxjs/toolkit'

interface Notification {
  id: string
  type: 'success' | 'error' | 'info'
  message: string
}

interface NotificationState {
  items: Notification[]
}

const initialState: NotificationState = {
  items: [],
}

const notificationSlice = createSlice({
  name: 'notification',
  initialState,
  reducers: {
    addNotification(state, action) {
      state.items.push(action.payload)
    },
    removeNotification(state, action) {
      state.items = state.items.filter((n) => n.id !== action.payload)
    },
    clearNotifications(state) {
      state.items = []
    },
  },
})

export const { addNotification, removeNotification, clearNotifications } =
  notificationSlice.actions
export default notificationSlice.reducer
