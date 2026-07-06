import React, { useState } from 'react'
import Sidebar from './Sidebar'
import Header from './Header'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  return (
    <div className="d-flex">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
      
      {/* Contenido principal */}
      <div className="flex-grow-1 d-flex flex-column">
        {/* Header */}
        <Header onMenuToggle={toggleSidebar} />
        
        {/* Contenido */}
        <main className="flex-grow-1 p-4">
          <div className="container-fluid">
            {children}
          </div>
        </main>
      </div>
      
      {/* Overlay para móvil */}
      {sidebarOpen && (
        <div 
          className="d-md-none position-fixed w-100 h-100 bg-dark bg-opacity-50"
          style={{ top: 0, left: 0, zIndex: 999 }}
          onClick={toggleSidebar}
        />
      )}
    </div>
  )
}

export default Layout 