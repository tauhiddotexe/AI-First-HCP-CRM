import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { hcpApi } from '@/services/api'
import type { HCP } from '@/types'

interface HCPState {
  list: HCP[]
  loading: boolean
  error: string | null
}

const initialState: HCPState = {
  list: [],
  loading: false,
  error: null,
}

export const fetchHCPs = createAsyncThunk('hcp/fetchAll', async () => {
  return await hcpApi.list()
})

const hcpSlice = createSlice({
  name: 'hcp',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchHCPs.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchHCPs.fulfilled, (state, action) => {
        state.loading = false
        state.list = action.payload
      })
      .addCase(fetchHCPs.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to load HCPs'
      })
  },
})

export default hcpSlice.reducer
