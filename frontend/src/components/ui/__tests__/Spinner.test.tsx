import { render, screen } from '@testing-library/react'
import { Spinner } from '../Spinner'

describe('Spinner', () => {
  it('renders with default md size', () => {
    render(<Spinner />)
    const svg = screen.getByRole('status')
    expect(svg).toBeInTheDocument()
    expect(svg.getAttribute('class')).toContain('h-5 w-5')
  })

  it('renders with sm size', () => {
    render(<Spinner size="sm" />)
    const svg = screen.getByRole('status')
    expect(svg.getAttribute('class')).toContain('h-4 w-4')
  })

  it('renders with lg size', () => {
    render(<Spinner size="lg" />)
    const svg = screen.getByRole('status')
    expect(svg.getAttribute('class')).toContain('h-6 w-6')
  })

  it('applies custom className', () => {
    render(<Spinner className="custom-class" />)
    const svg = screen.getByRole('status')
    expect(svg.getAttribute('class')).toContain('custom-class')
  })
})