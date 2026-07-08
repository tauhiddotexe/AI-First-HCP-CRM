import { useFormContext, useFieldArray } from 'react-hook-form'
import { Button, Input } from '@/components/ui'
import { Plus, X, BookOpen, Beaker } from 'lucide-react'

export function MaterialsSection() {
  const { register, control } = useFormContext()
  const materials = useFieldArray({ control, name: 'materials_shared' })
  const samples = useFieldArray({ control, name: 'samples_distributed' })

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <label className="text-xs font-medium text-surface-600 tracking-wide uppercase flex items-center gap-1.5">
          <BookOpen className="h-3.5 w-3.5" />
          Materials Shared
        </label>
        <div className="space-y-2">
          {materials.fields.map((field, index) => (
            <div key={field.id} className="flex gap-2 items-center">
              <Input {...register(`materials_shared.${index}.material_name`)} placeholder="Material name..." />
              <Input {...register(`materials_shared.${index}.quantity`)} type="number" placeholder="Qty" className="w-20 text-center" />
              <button
                type="button"
                onClick={() => materials.remove(index)}
                className="h-10 w-10 rounded-xl border border-surface-200 text-surface-400 hover:text-red-500 hover:border-red-200 hover:bg-red-50 flex items-center justify-center transition-all duration-150 flex-shrink-0"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
        <Button type="button" variant="ghost" size="sm" onClick={() => materials.append({ material_name: '', quantity: 1 })}>
          <Plus className="h-4 w-4" /> Add Material
        </Button>
      </div>

      <div className="space-y-2">
        <label className="text-xs font-medium text-surface-600 tracking-wide uppercase flex items-center gap-1.5">
          <Beaker className="h-3.5 w-3.5" />
          Samples Distributed
        </label>
        <div className="space-y-2">
          {samples.fields.map((field, index) => (
            <div key={field.id} className="flex gap-2 items-center">
              <Input {...register(`samples_distributed.${index}.product_name`)} placeholder="Product name..." />
              <Input {...register(`samples_distributed.${index}.quantity`)} type="number" placeholder="Qty" className="w-20 text-center" />
              <button
                type="button"
                onClick={() => samples.remove(index)}
                className="h-10 w-10 rounded-xl border border-surface-200 text-surface-400 hover:text-red-500 hover:border-red-200 hover:bg-red-50 flex items-center justify-center transition-all duration-150 flex-shrink-0"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
        <Button type="button" variant="ghost" size="sm" onClick={() => samples.append({ product_name: '', quantity: 1 })}>
          <Plus className="h-4 w-4" /> Add Sample
        </Button>
      </div>
    </div>
  )
}