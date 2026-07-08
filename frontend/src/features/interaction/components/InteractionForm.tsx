import { useEffect } from 'react'
import { useForm, FormProvider } from 'react-hook-form'
import { useAppSelector } from '@/redux/store'
import { InteractionDetailsSection } from './InteractionDetailsSection'
import { ParticipantsSection } from './ParticipantsSection'
import { DiscussionSection } from './DiscussionSection'
import { MaterialsSection } from './MaterialsSection'
import { AssessmentSection } from './AssessmentSection'
import { PlanningSection } from './PlanningSection'
import { Button } from '@/components/ui'
import { Save, FileText } from 'lucide-react'
import { motion } from 'framer-motion'

const defaultValues = {
  hcp_id: '',
  interaction_type: '',
  interaction_date: '',
  interaction_time: '',
  location: '',
  summary: '',
  sentiment: '',
  outcome: '',
  attendees: [{ name: '', role: '' }],
  discussion_topics: [{ topic: '' }],
  products_discussed: [{ product_name: '' }],
  materials_shared: [{ material_name: '', quantity: 1 }],
  samples_distributed: [{ product_name: '', quantity: 1 }],
  follow_ups: [{ action: '', follow_up_date: '', status: 'pending' }],
}

export function InteractionForm() {
  const { saving, current } = useAppSelector((s) => s.interaction)

  const methods = useForm({ defaultValues })

  useEffect(() => {
    if (current && Object.keys(current).length > 0) {
      methods.reset(current, { keepDefaultValues: true })
    }
  }, [current, methods])

  const onSubmit = methods.handleSubmit((data) => {
    console.log('Form data:', data)
  })

  const sections = [
    { id: 'details', label: 'Interaction Details', icon: FileText, component: <InteractionDetailsSection /> },
    { id: 'participants', label: 'Participants', icon: null, component: <ParticipantsSection /> },
    { id: 'discussion', label: 'Discussion', icon: null, component: <DiscussionSection /> },
    { id: 'materials', label: 'Materials', icon: null, component: <MaterialsSection /> },
    { id: 'assessment', label: 'Assessment', icon: null, component: <AssessmentSection /> },
    { id: 'planning', label: 'Planning', icon: null, component: <PlanningSection /> },
  ]

  return (
    <FormProvider {...methods}>
      <form onSubmit={onSubmit} className="h-full flex flex-col">
        <div className="flex items-center justify-between px-6 py-3.5 border-b border-surface-200 bg-white/80 backdrop-blur-xl flex-shrink-0">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-sm">
              <FileText className="h-4 w-4 text-white" />
            </div>
            <div>
              <h1 className="text-sm font-semibold text-surface-900 tracking-tight">Log HCP Interaction</h1>
              <p className="text-[11px] text-surface-400">AI-powered interaction logging</p>
            </div>
          </div>
          <Button type="submit" loading={saving} size="md">
            <Save className="h-4 w-4" />
            Save
          </Button>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-5 space-y-5">
          {sections.map((section, i) => (
            <motion.div
              key={section.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}
            >
              <div className="rounded-xl border border-surface-200 bg-white shadow-card overflow-hidden">
                <div className="px-5 py-3.5 border-b border-surface-100 bg-surface-50/50">
                  <h2 className="text-[11px] font-semibold text-surface-500 uppercase tracking-[0.08em]">
                    {section.label}
                  </h2>
                </div>
                <div className="px-5 py-4">
                  {section.component}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </form>
    </FormProvider>
  )
}