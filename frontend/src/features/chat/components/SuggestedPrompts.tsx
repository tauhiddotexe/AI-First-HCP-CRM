import { Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'

const prompts = [
  "Today I met Dr. Smith and discussed Product X. He was interested but concerned about pricing.",
  "I had a follow-up meeting with Dr. Patel. She's happy with the samples and wants more efficacy data.",
  "Met with Dr. Gupta at City Hospital. Discussed our new cardiovascular product line.",
]

interface SuggestedPromptsProps {
  onSelect: (prompt: string) => void
}

export function SuggestedPrompts({ onSelect }: SuggestedPromptsProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <div className="h-5 w-5 rounded-md bg-brand-50 border border-brand-200 flex items-center justify-center">
          <Sparkles className="h-3 w-3 text-brand-500" />
        </div>
        <span className="text-[10px] font-semibold text-surface-400 uppercase tracking-[0.1em]">Suggestions</span>
      </div>
      <div className="space-y-2">
        {prompts.map((prompt, i) => (
          <motion.button
            key={i}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, delay: i * 0.05, ease: [0.16, 1, 0.3, 1] }}
            onClick={() => onSelect(prompt)}
            className="w-full text-left text-sm text-surface-500 hover:text-surface-700 bg-white hover:bg-brand-50 border border-surface-200 hover:border-brand-200 rounded-xl px-4 py-3 transition-all duration-150 shadow-soft hover:shadow-card active:scale-[0.99] leading-relaxed"
          >
            {prompt}
          </motion.button>
        ))}
      </div>
    </div>
  )
}