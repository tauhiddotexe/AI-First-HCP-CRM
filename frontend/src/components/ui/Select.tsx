import { forwardRef } from 'react'
import type { SelectHTMLAttributes } from 'react'
import { ChevronDown } from 'lucide-react'

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  options: Array<{ value: string; label: string }>
  placeholder?: string
  aiUpdated?: boolean
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, options, placeholder, aiUpdated, className = '', ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label className="text-xs font-medium text-surface-600 tracking-wide uppercase">{label}</label>
        )}
        <div className="relative">
          <select
            ref={ref}
            className={`w-full appearance-none rounded-xl border border-surface-200 bg-white px-3.5 py-2.5 pr-10 text-sm text-surface-900 transition-all duration-150 focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-500/15 disabled:bg-surface-50 disabled:text-surface-400 ${
              error ? 'border-red-300 focus:border-red-400 focus:ring-red-500/15' : ''
            } ${props.value === '' || props.value === undefined ? 'text-surface-400' : ''} ${aiUpdated ? 'ai-updated' : ''} ${className}`}
            {...props}
          >
            {placeholder && <option value="" disabled>{placeholder}</option>}
            {options.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400 pointer-events-none" />
        </div>
        {error && <p className="text-xs text-red-500 font-medium">{error}</p>}
      </div>
    )
  },
)

Select.displayName = 'Select'