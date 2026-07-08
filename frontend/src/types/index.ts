export interface User {
  id: string
  full_name: string
  email: string
  role: 'sales_rep' | 'manager'
}

export interface HCP {
  id: string
  first_name: string
  last_name: string
  title?: string
  specialization?: string
  hospital?: string
  city?: string
  phone?: string
  email?: string
  created_at: string
}

export interface Interaction {
  id: string
  hcp_id: string
  hcp?: HCP
  user_id: string
  interaction_type: string
  interaction_date: string
  interaction_time?: string
  location?: string
  summary?: string
  sentiment?: string
  outcome?: string
  status: string
  hcp_name?: string
  date?: string
  attendees?: Attendee[]
  discussion_topics: DiscussionTopic[]
  products_discussed: ProductDiscussed[]
  materials_shared: MaterialShared[]
  samples_distributed: SampleDistributed[]
  follow_ups: FollowUp[]
  created_at: string
  updated_at: string
}

export interface Attendee {
  name: string
  role?: string
}

export interface DiscussionTopic {
  id: string
  interaction_id: string
  topic: string
}

export interface ProductDiscussed {
  id: string
  interaction_id: string
  product_name: string
}

export interface MaterialShared {
  id: string
  interaction_id: string
  material_name: string
  quantity: number
}

export interface SampleDistributed {
  id: string
  interaction_id: string
  product_name: string
  quantity: number
}

export interface FollowUp {
  id: string
  interaction_id: string
  follow_up_date?: string
  action: string
  status: 'pending' | 'completed' | 'cancelled'
}

export interface ChatMessage {
  id: string
  interaction_id?: string
  role: 'user' | 'assistant'
  message: string
  created_at: string
  tool_used?: string
}

export interface AgentChatRequest {
  message: string
  interaction_id?: string | null
}

export interface AgentChatResponse {
  assistant_message: string
  tool_used: string
  updated_form: Partial<Interaction>
  interaction_id: string
}

export interface ApiResponse<T> {
  success: boolean
  message: string
  data: T
}

export interface ApiError {
  success: false
  message: string
  errors?: Array<{ field: string; message: string }>
}

export interface PaginatedResponse<T> {
  items: T[]
  page: number
  limit: number
  total: number
  pages: number
}
