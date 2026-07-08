import type { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  className?: string
  hover?: boolean
}

export function Card({ children, className = '', hover = false }: CardProps) {
  return (
    <div
      className={`rounded-xl border border-surface-200 bg-white ${hover ? 'card-hover-effect cursor-pointer' : 'shadow-card'} ${className}`}
    >
      {children}
    </div>
  )
}