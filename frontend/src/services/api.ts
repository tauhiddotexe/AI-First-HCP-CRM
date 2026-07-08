import axios from 'axios'
import type { AxiosError } from 'axios'
import type {
  ApiResponse,
  ApiError,
  HCP,
  Interaction,
  AgentChatRequest,
  AgentChatResponse,
  ChatMessage,
  FollowUp,
  PaginatedResponse,
} from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
})

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    return Promise.reject(error)
  },
)

export const hcpApi = {
  list: () => api.get<HCP[]>('/hcps').then((r) => r.data),
  get: (id: string) => api.get<HCP>(`/hcps/${id}`).then((r) => r.data),
  create: (data: Partial<HCP>) => api.post<HCP>('/hcps', data).then((r) => r.data),
  update: (id: string, data: Partial<HCP>) =>
    api.patch<HCP>(`/hcps/${id}`, data).then((r) => r.data),
}

export const interactionApi = {
  list: (params?: Record<string, unknown>) =>
    api.get<PaginatedResponse<Interaction>>('/interactions', { params }).then((r) => r.data),
  get: (id: string) => api.get<Interaction>(`/interactions/${id}`).then((r) => r.data),
  create: (data: Partial<Interaction>) =>
    api.post<Interaction>('/interactions', data).then((r) => r.data),
  update: (id: string, data: Partial<Interaction>) =>
    api.patch<Interaction>(`/interactions/${id}`, data).then((r) => r.data),
  delete: (id: string) => api.delete(`/interactions/${id}`).then((r) => r.data),
}

export const agentApi = {
  chat: (data: AgentChatRequest) =>
    api.post<ApiResponse<AgentChatResponse>>('/agent/chat', data).then((r) => r.data),
}

export const chatApi = {
  history: (interactionId: string) =>
    api.get<ChatMessage[]>(`/chat/${interactionId}`).then((r) => r.data),
}

export const followUpApi = {
  list: () => api.get<FollowUp[]>('/followups').then((r) => r.data),
  create: (data: Partial<FollowUp>) => api.post<FollowUp>('/followups', data).then((r) => r.data),
  update: (id: string, data: Partial<FollowUp>) =>
    api.patch<FollowUp>(`/followups/${id}`, data).then((r) => r.data),
}

export const dashboardApi = {
  stats: () =>
    api
      .get<{
        total_interactions: number
        pending_followups: number
        hcp_count: number
      }>('/dashboard')
      .then((r) => r.data),
}

export default api
