import { useState } from 'react'
import { Users, Target, Megaphone, BarChart3, Menu, X } from 'lucide-react'
import CustomerManagement from './components/CustomerManagement'
import SalesManagement from './components/SalesManagement'
import MarketingModule from './components/MarketingModule'
import AnalyticsModule from './components/AnalyticsModule'
import './App.css'

type ActiveModule = 'customers' | 'sales' | 'marketing' | 'analytics'

function App() {
  const [activeModule, setActiveModule] = useState<ActiveModule>('customers')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const modules = [
    { id: 'customers' as const, name: 'Customers', icon: Users, component: CustomerManagement },
    { id: 'sales' as const, name: 'Sales Pipeline', icon: Target, component: SalesManagement },
    { id: 'marketing' as const, name: 'Marketing', icon: Megaphone, component: MarketingModule },
    { id: 'analytics' as const, name: 'Analytics', icon: BarChart3, component: AnalyticsModule },
  ]

  const ActiveComponent = modules.find(m => m.id === activeModule)?.component || CustomerManagement

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-16'} bg-white shadow-lg transition-all duration-300 flex flex-col`}>
        <div className="p-4 border-b">
          <div className="flex items-center justify-between">
            <h1 className={`font-bold text-xl text-gray-800 ${!sidebarOpen && 'hidden'}`}>
              CRM System
            </h1>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100"
            >
              {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>
        
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {modules.map((module) => {
              const Icon = module.icon
              return (
                <li key={module.id}>
                  <button
                    onClick={() => setActiveModule(module.id)}
                    className={`w-full flex items-center p-3 rounded-lg transition-colors ${
                      activeModule === module.id
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon size={20} />
                    {sidebarOpen && <span className="ml-3">{module.name}</span>}
                  </button>
                </li>
              )
            })}
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white shadow-sm border-b p-4">
          <h2 className="text-2xl font-semibold text-gray-800">
            {modules.find(m => m.id === activeModule)?.name}
          </h2>
        </header>
        
        <main className="flex-1 overflow-auto p-6">
          <ActiveComponent />
        </main>
      </div>
    </div>
  )
}

export default App
