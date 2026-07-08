import { createSlice } from '@reduxjs/toolkit'
import type { User } from '@/types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
}

const initialState: AuthState = {
  user: {
    id: 'demo-rep-001',
    full_name: 'Demo Representative',
    email: 'rep@pharma.com',
    role: 'sales_rep',
  },
  isAuthenticated: true,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {},
})

export default authSlice.reducer
