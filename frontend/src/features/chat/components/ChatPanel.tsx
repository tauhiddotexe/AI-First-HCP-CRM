import { useEffect, useRef, useState } from 'react'
import { useAppSelector, useAppDispatch } from '@/redux/store'
import { sendMessage, addMessage, clearLastResponse } from '@/redux/slices/chatSlice'
import { updateFormFromAI } from '@/redux/slices/interactionSlice'
import { setAiUpdatedFields } from '@/redux/slices/uiSlice'
import { MessageBubble } from './MessageBubble'
import { ChatInput } from './ChatInput'
import { SuggestedPrompts } from './SuggestedPrompts'
import { Bot, Sparkles } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

interface ChatPanelProps {
  interactionId?: string | null
}

export function ChatPanel({ interactionId }: ChatPanelProps) {
  const dispatch = useAppDispatch()
  const { messages, isProcessing, lastResponse } = useAppSelector((s) => s.chat)
  const scrollRef = useRef<HTMLDivElement>(null)
  const [showPrompts, setShowPrompts] = useState(true)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  useEffect(() => {
    const form = lastResponse?.updated_form
    if (form && Object.keys(form).length > 0) {
      dispatch(updateFormFromAI(form))
      const updatedFields = Object.keys(form).filter((k) => form[k as keyof typeof form] != null)
      dispatch(setAiUpdatedFields(updatedFields))
      dispatch(clearLastResponse())
      setTimeout(() => {
        dispatch(setAiUpdatedFields([]))
      }, 3000)
    }
  }, [lastResponse, dispatch])

  const handleSend = async (message: string) => {
    dispatch(addMessage({
      id: crypto.randomUUID(),
      role: 'user',
      message,
      created_at: new Date().toISOString(),
    }))
    setShowPrompts(false)
    try {
      await dispatch(sendMessage({ message, interaction_id: interactionId })).unwrap()
    } catch (err) {
      const msg = err instanceof Error ? err.message : typeof err === 'string' ? err : JSON.stringify(err)
      dispatch(addMessage({
        id: crypto.randomUUID(),
        role: 'assistant',
        message: `Sorry, I encountered an error: ${msg}`,
        created_at: new Date().toISOString(),
      }))
    }
  }

  const hasMessages = messages.length > 0

  return (
    <div className="flex flex-col h-full bg-surface-50">
      <div className="border-b border-surface-200 bg-white/80 backdrop-blur-xl px-5 py-3.5 flex items-center gap-3 flex-shrink-0">
        <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-sm">
          <Bot className="h-4 w-4 text-white" />
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="text-sm font-semibold text-surface-900 tracking-tight">AI Assistant</h2>
          <p className="text-[11px] text-surface-400">LangGraph + Groq</p>
        </div>
        <div className="flex items-center gap-1.5 text-[10px] font-medium text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-1 rounded-lg">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse-soft" />
          Online
        </div>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto px-5 py-5 space-y-4">
        <AnimatePresence mode="wait">
          {!hasMessages && !isProcessing && showPrompts && (
            <motion.div
              key="empty-state"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            >
              <div className="pt-6">
                <div className="flex flex-col items-center text-center mb-6">
                  <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-brand-50 to-brand-100 flex items-center justify-center mb-4 ring-4 ring-brand-50/50 shadow-card">
                    <Sparkles className="h-7 w-7 text-brand-500" />
                  </div>
                  <p className="text-base font-semibold text-surface-900 tracking-tight">How can I help you?</p>
                  <p className="text-sm text-surface-400 mt-1.5 max-w-xs leading-relaxed">
                    Describe your HCP interaction naturally and I&apos;ll log it in the CRM.
                  </p>
                </div>
                <div className="max-w-sm mx-auto">
                  <SuggestedPrompts onSelect={handleSend} />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
        </AnimatePresence>

        {isProcessing && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex gap-3"
          >
            <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-surface-100 border border-surface-200 flex items-center justify-center">
              <Bot className="h-4 w-4 text-surface-500" />
            </div>
            <div className="bg-white border border-surface-200 rounded-2xl rounded-tl-md px-4 py-3 shadow-card flex items-center gap-2">
              <span className="flex gap-1">
                <span className="h-2 w-2 rounded-full bg-brand-400 animate-pulse-soft" style={{ animationDelay: '0ms' }} />
                <span className="h-2 w-2 rounded-full bg-brand-400 animate-pulse-soft" style={{ animationDelay: '300ms' }} />
                <span className="h-2 w-2 rounded-full bg-brand-400 animate-pulse-soft" style={{ animationDelay: '600ms' }} />
              </span>
            </div>
          </motion.div>
        )}

        {hasMessages && messages[messages.length - 1]?.role === 'assistant' && !isProcessing && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="pt-2"
          >
            <SuggestedPrompts onSelect={handleSend} />
          </motion.div>
        )}
      </div>

      <ChatInput onSend={handleSend} disabled={isProcessing} />
    </div>
  )
}