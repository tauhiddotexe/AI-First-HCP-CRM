import { useFormContext, useFieldArray } from 'react-hook-form'
import { Button, Input } from '@/components/ui'
import { Plus, X, MessageSquare, Package } from 'lucide-react'

export function DiscussionSection() {
  const { register, control } = useFormContext()
  const topics = useFieldArray({ control, name: 'discussion_topics' })
  const products = useFieldArray({ control, name: 'products_discussed' })

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <label className="text-xs font-medium text-surface-600 tracking-wide uppercase flex items-center gap-1.5">
          <MessageSquare className="h-3.5 w-3.5" />
          Topics Discussed
        </label>
        <div className="space-y-2">
          {topics.fields.map((field, index) => (
            <div key={field.id} className="flex gap-2 items-center">
              <Input {...register(`discussion_topics.${index}.topic`)} placeholder="Enter topic..." />
              <button
                type="button"
                onClick={() => topics.remove(index)}
                className="h-10 w-10 rounded-xl border border-surface-200 text-surface-400 hover:text-red-500 hover:border-red-200 hover:bg-red-50 flex items-center justify-center transition-all duration-150 flex-shrink-0"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
        <Button type="button" variant="ghost" size="sm" onClick={() => topics.append({ topic: '' })}>
          <Plus className="h-4 w-4" /> Add Topic
        </Button>
      </div>

      <div className="space-y-2">
        <label className="text-xs font-medium text-surface-600 tracking-wide uppercase flex items-center gap-1.5">
          <Package className="h-3.5 w-3.5" />
          Products Discussed
        </label>
        <div className="space-y-2">
          {products.fields.map((field, index) => (
            <div key={field.id} className="flex gap-2 items-center">
              <Input {...register(`products_discussed.${index}.product_name`)} placeholder="Enter product name..." />
              <button
                type="button"
                onClick={() => products.remove(index)}
                className="h-10 w-10 rounded-xl border border-surface-200 text-surface-400 hover:text-red-500 hover:border-red-200 hover:bg-red-50 flex items-center justify-center transition-all duration-150 flex-shrink-0"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
        <Button type="button" variant="ghost" size="sm" onClick={() => products.append({ product_name: '' })}>
          <Plus className="h-4 w-4" /> Add Product
        </Button>
      </div>
    </div>
  )
}