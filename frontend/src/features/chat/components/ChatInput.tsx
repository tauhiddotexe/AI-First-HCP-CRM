import { useState, useRef, useEffect } from 'react'
import { ArrowUp } from 'lucide-react'

interface ChatInputProps {
  onSend: (message: string) => void
  disabled?: boolean
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`
    }
  }, [input])

  const handleSubmit = () => {
    const trimmed = input.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setInput('')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const hasText = input.trim().length > 0

  return (
    <div className="border-t border-surface-200 bg-white/80 backdrop-blur-xl px-5 py-4">
      <div className="flex gap-2.5 items-end">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe your interaction..."
          rows={1}
          className="flex-1 rounded-xl border border-surface-200 px-4 py-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-brand-500/15 focus:border-brand-400 bg-surface-50 placeholder:text-surface-400 transition-all duration-150"
          disabled={disabled}
        />
        <button
          onClick={handleSubmit}
          disabled={!hasText || disabled}
          className={`h-[46px] w-[46px] rounded-xl flex items-center justify-center shrink-0 transition-all duration-150 active:scale-[0.93] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 ${
            hasText && !disabled
            ? 'bg-brand-600 text-white hover:bg-brand-700 shadow-soft'
            : 'bg-surface-100 text-surface-400 cursor-not-allowed'
          }`}
        >
          <ArrowUp className="h-5 w-5" />
        </button>
      </div>
    </div>
  )
}