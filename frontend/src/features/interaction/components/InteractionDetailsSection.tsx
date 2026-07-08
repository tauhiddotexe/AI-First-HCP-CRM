import { useFormContext } from 'react-hook-form'
import { Input, Select } from '@/components/ui'
import { HCPSelect } from './HCPSelect'

const interactionTypes = [
  { value: 'Face-to-Face', label: 'Face to Face' },
  { value: 'Virtual', label: 'Virtual' },
  { value: 'Phone Call', label: 'Phone Call' },
  { value: 'Email', label: 'Email' },
  { value: 'Group Meeting', label: 'Group Meeting' },
  { value: 'Conference', label: 'Conference' },
]

export function InteractionDetailsSection() {
  const { register, formState: { errors } } = useFormContext()

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <HCPSelect />
        <Select
          label="Interaction Type"
          placeholder="Select type..."
          options={interactionTypes}
          error={errors.interaction_type?.message as string}
          {...register('interaction_type', { required: 'Type is required' })}
        />
        <Input
          label="Date"
          type="date"
          error={errors.interaction_date?.message as string}
          {...register('interaction_date', { required: 'Date is required' })}
        />
        <Input
          label="Time"
          type="time"
          {...register('interaction_time')}
        />
      </div>
    </div>
  )
}