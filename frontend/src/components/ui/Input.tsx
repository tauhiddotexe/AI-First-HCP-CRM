import { forwardRef } from 'react'
import type { InputHTMLAttributes } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  aiUpdated?: boolean
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, aiUpdated, className = '', ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label className="text-xs font-medium text-surface-600 tracking-wide uppercase">{label}</label>
        )}
        <input
          ref={ref}
          className={`w-full rounded-xl border border-surface-200 bg-white px-3.5 py-2.5 text-sm text-surface-900 placeholder:text-surface-400 transition-all duration-150 focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-500/15 disabled:bg-surface-50 disabled:text-surface-400 ${
            error ? 'border-red-300 focus:border-red-400 focus:ring-red-500/15' : ''
          } ${aiUpdated ? 'ai-updated' : ''} ${className}`}
          {...props}
        />
        {error && <p className="text-xs text-red-500 font-medium">{error}</p>}
      </div>
    )
  },
)

Input.displayName = 'Input'