import type { ChatMessage } from '@/types'
import { Bot, User } from 'lucide-react'
import { motion } from 'framer-motion'

interface MessageBubbleProps {
  message: ChatMessage
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, y: 12, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center ${
          isUser
            ? 'bg-brand-100 text-brand-600 border border-brand-200'
            : 'bg-surface-100 text-surface-500 border border-surface-200'
        }`}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>
      <div className={`max-w-[85%] ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
        <div
          className={`rounded-2xl px-4 py-3 text-sm leading-relaxed ${
            isUser
              ? 'bg-brand-600 text-white rounded-tr-md shadow-soft'
              : 'bg-white border border-surface-200 text-surface-700 rounded-tl-md shadow-card'
          }`}
        >
          {message.message}
        </div>
        {message.tool_used && (
          <span className="text-[10px] text-surface-400 mt-1.5 px-1 font-medium tracking-wide">
            via {message.tool_used.replace(/_/g, ' ')}
          </span>
        )}
      </div>
    </motion.div>
  )
}