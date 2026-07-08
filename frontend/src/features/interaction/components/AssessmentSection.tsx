import { useFormContext } from 'react-hook-form'
import { Textarea } from '@/components/ui'
import { Frown, Meh, Smile } from 'lucide-react'
import { motion } from 'framer-motion'

const sentiments = [
  { value: 'Positive', icon: Smile, color: 'text-emerald-500', selectedBg: 'bg-emerald-50 border-emerald-300', ring: 'ring-emerald-500' },
  { value: 'Neutral', icon: Meh, color: 'text-amber-500', selectedBg: 'bg-amber-50 border-amber-300', ring: 'ring-amber-500' },
  { value: 'Negative', icon: Frown, color: 'text-red-500', selectedBg: 'bg-red-50 border-red-300', ring: 'ring-red-500' },
]

export function AssessmentSection() {
  const { register, watch, setValue } = useFormContext()
  const sentiment = watch('sentiment')
  const inferred = watch('sentiment_source') || 'observed'

  return (
    <div className="space-y-5">
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-medium text-surface-600 tracking-wide uppercase">
            HCP Sentiment
          </label>
          <div className="flex items-center gap-1 bg-surface-100 rounded-lg p-0.5">
            <button
              type="button"
              onClick={() => setValue('sentiment_source', 'observed')}
              className={`text-[11px] px-2.5 py-1 rounded-md transition-all duration-150 font-medium ${
                inferred === 'observed' ? 'bg-white text-surface-900 shadow-soft' : 'text-surface-400 hover:text-surface-600'
              }`}
            >
              Observed
            </button>
            <button
              type="button"
              onClick={() => setValue('sentiment_source', 'inferred')}
              className={`text-[11px] px-2.5 py-1 rounded-md transition-all duration-150 font-medium ${
                inferred === 'inferred' ? 'bg-white text-surface-900 shadow-soft' : 'text-surface-400 hover:text-surface-600'
              }`}
            >
              Inferred
            </button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2.5">
          {sentiments.map((s) => {
            const Icon = s.icon
            const selected = sentiment === s.value
            return (
              <motion.button
                key={s.value}
                type="button"
                onClick={() => setValue('sentiment', s.value, { shouldValidate: true })}
                whileTap={{ scale: 0.97 }}
                className={`flex flex-col items-center gap-1.5 rounded-xl border px-3 py-3 transition-all duration-150 ${
                  selected
                    ? `${s.selectedBg} ${s.color} border-current`
                    : 'border-surface-200 text-surface-400 hover:border-surface-300 hover:text-surface-500 hover:bg-surface-50 bg-white'
                }`}
              >
                <Icon className={`h-5 w-5 ${selected ? s.color : ''}`} />
                <span className="text-[11px] font-semibold">{s.value}</span>
              </motion.button>
            )
          })}
        </div>
        <input type="hidden" {...register('sentiment_source')} />
      </div>

      <div className="space-y-2">
        <label className="text-xs font-medium text-surface-600 tracking-wide uppercase">Outcomes</label>
        <Textarea
          placeholder="Describe the outcome of the interaction..."
          rows={3}
          {...register('outcome')}
        />
      </div>
    </div>
  )
}