import { useFormContext, useFieldArray } from 'react-hook-form'
import { Button, Input } from '@/components/ui'
import { Plus, X, Users } from 'lucide-react'

export function ParticipantsSection() {
  const { control, register } = useFormContext()
  const attendees = useFieldArray({ control, name: 'attendees' })

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <label className="text-xs font-medium text-surface-600 tracking-wide uppercase">Attendees</label>
        {attendees.fields.length === 0 && (
          <div className="flex items-center gap-2 text-sm text-surface-400 bg-surface-50 rounded-xl px-3.5 py-3 border border-surface-100">
            <Users className="h-4 w-4" />
            <span>No additional attendees</span>
          </div>
        )}
        <div className="space-y-2">
          {attendees.fields.map((field, index) => (
            <div key={field.id} className="flex gap-2 items-center">
              <Input {...register(`attendees.${index}.name`)} placeholder="Attendee name..." />
              <Input {...register(`attendees.${index}.role`)} placeholder="Role..." />
              <button
                type="button"
                onClick={() => attendees.remove(index)}
                className="h-10 w-10 rounded-xl border border-surface-200 text-surface-400 hover:text-red-500 hover:border-red-200 hover:bg-red-50 flex items-center justify-center transition-all duration-150 flex-shrink-0"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
        <Button type="button" variant="ghost" size="sm" onClick={() => attendees.append({ name: '', role: '' })}>
          <Plus className="h-4 w-4" /> Add Attendee
        </Button>
      </div>
    </div>
  )
}