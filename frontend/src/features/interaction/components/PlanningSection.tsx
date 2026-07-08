import { useFormContext, useFieldArray } from 'react-hook-form'
import { Button, Input, Textarea } from '@/components/ui'
import { Plus, X, CalendarCheck } from 'lucide-react'

export function PlanningSection() {
  const { register, control } = useFormContext()
  const followUps = useFieldArray({ control, name: 'follow_ups' })

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <label className="text-xs font-medium text-surface-600 tracking-wide uppercase flex items-center gap-1.5">
          <CalendarCheck className="h-3.5 w-3.5" />
          Follow-up Actions
        </label>
        <div className="space-y-2">
          {followUps.fields.map((field, index) => (
            <div key={field.id} className="flex gap-2 items-start">
              <div className="flex-1 grid grid-cols-2 gap-2">
                <Input {...register(`follow_ups.${index}.action`)} placeholder="Action..." />
                <Input {...register(`follow_ups.${index}.follow_up_date`)} type="date" />
              </div>
              <button
                type="button"
                onClick={() => followUps.remove(index)}
                className="h-10 w-10 rounded-xl border border-surface-200 text-surface-400 hover:text-red-500 hover:border-red-200 hover:bg-red-50 flex items-center justify-center transition-all duration-150 flex-shrink-0 mt-0"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
        <Button type="button" variant="ghost" size="sm" onClick={() => followUps.append({ action: '', follow_up_date: '', status: 'pending' })}>
          <Plus className="h-4 w-4" /> Add Follow-up
        </Button>
      </div>

      <div className="pt-2">
        <Textarea label="Additional Notes" placeholder="Enter any additional notes..." rows={4} {...register('summary')} />
      </div>
    </div>
  )
}