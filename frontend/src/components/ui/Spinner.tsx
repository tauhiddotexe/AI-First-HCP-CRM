import { Loader2 } from 'lucide-react'

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const sizes = {
  sm: 'h-4 w-4',
  md: 'h-5 w-5',
  lg: 'h-6 w-6',
}

export function Spinner({ size = 'md', className = '' }: SpinnerProps) {
  return (
    <Loader2
      role="status"
      className={`animate-spin text-brand-500 ${sizes[size]} ${className}`}
      aria-label="Loading"
    />
  )
}