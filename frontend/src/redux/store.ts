import { configureStore } from '@reduxjs/toolkit'
import { useDispatch, useSelector } from 'react-redux'
import type { TypedUseSelectorHook } from 'react-redux'
import authReducer from './slices/authSlice'
import chatReducer from './slices/chatSlice'
import interactionReducer from './slices/interactionSlice'
import hcpReducer from './slices/hcpSlice'
import agentReducer from './slices/agentSlice'
import uiReducer from './slices/uiSlice'
import notificationReducer from './slices/notificationSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    chat: chatReducer,
    interaction: interactionReducer,
    hcp: hcpReducer,
    agent: agentReducer,
    ui: uiReducer,
    notification: notificationReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

export const useAppDispatch: () => AppDispatch = useDispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
