import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { interactionApi } from '@/services/api'
import type { Interaction, FollowUp } from '@/types'

interface InteractionState {
  current: Partial<Interaction> | null
  followUps: FollowUp[]
  loading: boolean
  saving: boolean
  savingField: string | null
  error: string | null
}

const initialState: InteractionState = {
  current: null,
  followUps: [],
  loading: false,
  saving: false,
  savingField: null,
  error: null,
}

export const saveInteraction = createAsyncThunk(
  'interaction/save',
  async (data: Partial<Interaction>) => {
    const response = await interactionApi.create(data)
    return response
  },
)

export const updateInteraction = createAsyncThunk(
  'interaction/update',
  async ({ id, data }: { id: string; data: Partial<Interaction> }) => {
    const response = await interactionApi.update(id, data)
    return response
  },
)

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    setInteraction(state, action) {
      state.current = action.payload
    },
    updateFormFromAI(state, action) {
      const aiData = action.payload as Record<string, unknown>
      const current = state.current ? { ...state.current } : {} as Partial<Interaction>

      const fieldMap: Record<string, string> = {
        hcp_name: 'hcp_name',
        interaction_type: 'interaction_type',
        date: 'interaction_date',
        sentiment: 'sentiment',
        summary: 'summary',
        outcome: 'outcome',
        discussion_topics: 'discussion_topics',
        products_discussed: 'products_discussed',
        materials_shared: 'materials_shared',
        samples_distributed: 'samples_distributed',
      }

      for (const [aiField, stateField] of Object.entries(fieldMap)) {
        if (aiData[aiField] != null) {
          (current as Record<string, unknown>)[stateField] = aiData[aiField]
        }
      }

      state.current = current
    },
    updateFormField(state, action) {
      const { field, value } = action.payload
      if (state.current) {
        state.current = { ...state.current, [field]: value }
      }
    },
    setSavingField(state, action) {
      state.savingField = action.payload
    },
    clearInteraction(state) {
      state.current = null
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(saveInteraction.pending, (state) => {
        state.saving = true
        state.error = null
      })
      .addCase(saveInteraction.fulfilled, (state, action) => {
        state.saving = false
        state.current = action.payload
      })
      .addCase(saveInteraction.rejected, (state, action) => {
        state.saving = false
        state.error = action.error.message || 'Failed to save'
      })
      .addCase(updateInteraction.pending, (state) => {
        state.saving = true
      })
      .addCase(updateInteraction.fulfilled, (state, action) => {
        state.saving = false
        state.current = action.payload
        state.savingField = null
      })
      .addCase(updateInteraction.rejected, (state, action) => {
        state.saving = false
        state.error = action.error.message || 'Failed to update'
      })
  },
})

export const { setInteraction, updateFormFromAI, updateFormField, setSavingField, clearInteraction } =
  interactionSlice.actions
export default interactionSlice.reducer
