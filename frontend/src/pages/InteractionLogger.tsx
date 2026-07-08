import { InteractionForm } from '@/features/interaction/components/InteractionForm'
import { ChatPanel } from '@/features/chat/components/ChatPanel'

export function InteractionLogger() {
  return (
    <div className="flex h-full w-full">
      <div className="w-[65%] h-full overflow-hidden border-r border-surface-200 bg-white">
        <InteractionForm />
      </div>
      <div className="w-[35%] h-full overflow-hidden">
        <ChatPanel />
      </div>
    </div>
  )
}