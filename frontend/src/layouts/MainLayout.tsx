import { Outlet, Link } from 'react-router-dom'
import { Database, Activity } from 'lucide-react'

export function MainLayout() {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-surface-50 font-inter">
      <div className="flex flex-col flex-1 w-full">
        <header className="h-14 flex-shrink-0 border-b border-surface-200 bg-white/80 backdrop-blur-xl flex items-center justify-between px-6 z-10">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-sm">
              <Database className="h-4 w-4 text-white" />
            </div>
            <div className="h-5 w-px bg-surface-200" />
            <Link to="/" className="flex items-center gap-1.5">
              <span className="text-sm font-semibold text-surface-900 tracking-tight">CRM</span>
              <span className="text-[10px] font-medium text-brand-500 bg-brand-50 px-1.5 py-0.5 rounded-md uppercase tracking-wider">AI</span>
            </Link>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-xs text-surface-400 bg-surface-50 px-2.5 py-1.5 rounded-lg">
              <Activity className="h-3.5 w-3.5" />
              <span>Live</span>
            </div>
            <div className="h-7 w-7 rounded-full bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center text-[10px] font-semibold text-white shadow-sm">
              MR
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-hidden">
          <Outlet />
        </main>
      </div>
    </div>
  )
}