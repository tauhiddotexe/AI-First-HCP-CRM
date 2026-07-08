import { Routes, Route, Navigate } from 'react-router-dom'
import { MainLayout } from '@/layouts/MainLayout'
import { InteractionLogger } from '@/pages/InteractionLogger'

export function AppRouter() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Navigate to="/interactions/new" replace />} />
        <Route path="/interactions/new" element={<InteractionLogger />} />
        <Route path="/interactions/:id" element={<InteractionLogger />} />
      </Route>
    </Routes>
  )
}
