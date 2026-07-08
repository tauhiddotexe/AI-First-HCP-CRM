import { useEffect, useState, useRef } from 'react'
import { useFormContext } from 'react-hook-form'
import { useAppSelector, useAppDispatch } from '@/redux/store'
import { fetchHCPs } from '@/redux/slices/hcpSlice'
import { Search, Check, ChevronDown, Stethoscope } from 'lucide-react'

export function HCPSelect() {
  const dispatch = useAppDispatch()
  const { list: hcps, loading } = useAppSelector((s) => s.hcp)
  const { register, setValue, watch } = useFormContext()
  const [search, setSearch] = useState('')
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    dispatch(fetchHCPs())
  }, [dispatch])

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  const filtered = hcps.filter(
    (h) =>
      `${h.first_name} ${h.last_name} ${h.hospital || ''} ${h.specialization || ''}`
        .toLowerCase()
        .includes(search.toLowerCase()),
  )

  const selectedHcp = hcps.find((h) => h.id === watch('hcp_id'))

  return (
    <div ref={ref} className="flex flex-col gap-1.5 relative">
      <label className="text-xs font-medium text-surface-600 tracking-wide uppercase">HCP</label>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full rounded-xl border border-surface-200 bg-white px-3.5 py-2.5 text-sm text-left flex items-center justify-between gap-2 transition-all duration-150 hover:border-surface-300 focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-500/15"
      >
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="h-6 w-6 rounded-lg bg-surface-100 flex items-center justify-center flex-shrink-0">
            <Stethoscope className="h-3.5 w-3.5 text-surface-500" />
          </div>
          <span className={selectedHcp ? 'text-surface-900 font-medium truncate' : 'text-surface-400 truncate'}>
            {selectedHcp ? `Dr. ${selectedHcp.first_name} ${selectedHcp.last_name}` : 'Select HCP...'}
          </span>
        </div>
        <ChevronDown className={`h-4 w-4 text-surface-400 flex-shrink-0 transition-transform duration-150 ${open ? 'rotate-180' : ''}`} />
      </button>
      <input type="hidden" {...register('hcp_id', { required: 'HCP is required' })} />

      {open && (
        <div className="absolute z-50 mt-1 w-full bg-white border border-surface-200 rounded-xl shadow-elevated max-h-64 overflow-hidden dropdown-enter top-full">
          <div className="p-2 border-b border-surface-100">
            <div className="flex items-center gap-2 bg-surface-50 rounded-lg px-3 py-1.5">
              <Search className="h-4 w-4 text-surface-400 flex-shrink-0" />
              <input
                autoFocus
                placeholder="Search HCPs..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="bg-transparent text-sm text-surface-900 placeholder:text-surface-400 w-full focus:outline-none"
              />
            </div>
          </div>
          <div className="overflow-y-auto max-h-48">
            {loading && (
              <div className="px-3 py-5 text-xs text-surface-400 text-center">Loading...</div>
            )}
            {!loading && filtered.length === 0 && (
              <div className="px-3 py-5 text-xs text-surface-400 text-center">No HCPs found</div>
            )}
            {filtered.map((hcp) => (
              <button
                key={hcp.id}
                type="button"
                onClick={() => {
                  setValue('hcp_id', hcp.id, { shouldValidate: true })
                  setOpen(false)
                  setSearch('')
                }}
                className="w-full px-3 py-2.5 text-sm text-left hover:bg-brand-50 active:bg-brand-100 flex items-center justify-between gap-2 transition-colors duration-100"
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <div className="h-6 w-6 rounded-full bg-brand-100 flex items-center justify-center flex-shrink-0">
                    <Stethoscope className="h-3 w-3 text-brand-600" />
                  </div>
                  <div className="min-w-0">
                    <span className="text-surface-900 font-medium text-sm">
                      Dr. {hcp.first_name} {hcp.last_name}
                    </span>
                    <div className="flex items-center gap-1.5 flex-wrap">
                      {hcp.specialization && (
                        <span className="text-[11px] text-surface-400">{hcp.specialization}</span>
                      )}
                      {hcp.hospital && (
                        <span className="text-[11px] text-surface-400">· {hcp.hospital}</span>
                      )}
                    </div>
                  </div>
                </div>
                {selectedHcp?.id === hcp.id && (
                  <Check className="h-4 w-4 text-brand-500 flex-shrink-0" />
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}