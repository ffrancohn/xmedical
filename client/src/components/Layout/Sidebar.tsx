import React from 'react'
import { Link, useLocation } from 'wouter'
import { useAuth } from '@/contexts/AuthContext'
import { useTheme } from '@/contexts/ThemeContext'
import { 
  Home, 
  User, 
  FileText, 
  MapPin, 
  Users, 
  MessageSquare, 
  Settings,
  Moon,
  Sun,
  Palette,
  LogOut,
  Menu,
  X
} from 'lucide-react'
import { MenuItem } from '@/types'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onToggle }) => {
  const { user, logout } = useAuth()
  const { theme, toggleMode, setColor } = useTheme()
  const [location] = useLocation()

  const menuItems: MenuItem[] = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: 'Home',
      path: '/dashboard'
    },
    {
      id: 'profile',
      label: 'Perfil',
      icon: 'User',
      path: '/profile'
    },
    {
      id: 'documents',
      label: 'Documentos',
      icon: 'FileText',
      path: '/documents'
    },
    {
      id: 'addresses',
      label: 'Direcciones',
      icon: 'MapPin',
      path: '/addresses'
    },
    {
      id: 'beneficiaries',
      label: 'Beneficiarios',
      icon: 'Users',
      path: '/beneficiaries'
    },
    {
      id: 'feedback',
      label: 'Feedback',
      icon: 'MessageSquare',
      path: '/feedback'
    },
    {
      id: 'admin',
      label: 'Administración',
      icon: 'Settings',
      path: '/admin',
      requiresAdmin: true
    }
  ]

  const colorOptions = [
    { value: 'blue', label: 'Azul', class: 'bg-primary' },
    { value: 'green', label: 'Verde', class: 'bg-success' },
    { value: 'purple', label: 'Púrpura', class: 'bg-purple' },
    { value: 'orange', label: 'Naranja', class: 'bg-warning' },
    { value: 'red', label: 'Rojo', class: 'bg-danger' },
    { value: 'slate', label: 'Gris', class: 'bg-secondary' }
  ]

  const getIconComponent = (iconName: string) => {
    const icons: { [key: string]: React.ComponentType<any> } = {
      Home,
      User,
      FileText,
      MapPin,
      Users,
      MessageSquare,
      Settings
    }
    return icons[iconName] || Home
  }

  const handleLogout = () => {
    logout()
  }

  return (
    <>
      {/* Botón de menú para móvil */}
      <button
        className="btn btn-link d-md-none position-fixed"
        style={{ top: '1rem', left: '1rem', zIndex: 1001 }}
        onClick={onToggle}
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <div className={`sidebar ${isOpen ? 'show' : ''} d-md-block`} style={{ width: '280px', minHeight: '100vh' }}>
        <div className="p-3">
          {/* Logo */}
          <div className="text-center mb-4">
            <h4 className="text-gradient fw-bold mb-0">XMedical</h4>
            <small className="text-muted">Asistente Médico Inteligente</small>
          </div>

          {/* Información del usuario */}
          {user && (
            <div className="card mb-4">
              <div className="card-body text-center">
                <div className="bg-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-2" style={{ width: '48px', height: '48px' }}>
                  <User size={24} className="text-white" />
                </div>
                <h6 className="mb-1">{user.fullName}</h6>
                <small className="text-muted">{user.email}</small>
              </div>
            </div>
          )}

          {/* Navegación */}
          <nav className="sidebar-nav">
            <ul className="nav flex-column">
              {menuItems.map((item) => {
                // Ocultar elementos que requieren admin si el usuario no es admin
                if (item.requiresAdmin && user?.profileId !== 1) {
                  return null
                }

                const IconComponent = getIconComponent(item.icon)
                const isActive = location === item.path

                return (
                  <li key={item.id} className="nav-item">
                    <Link href={item.path}>
                      <a className={`nav-link ${isActive ? 'active' : ''}`}>
                        <IconComponent size={20} className="me-2" />
                        {item.label}
                      </a>
                    </Link>
                  </li>
                )
              })}
            </ul>
          </nav>

          {/* Configuración de tema */}
          <div className="mt-4">
            <h6 className="text-muted mb-3">Configuración</h6>
            
            {/* Toggle modo oscuro/claro */}
            <div className="d-flex align-items-center justify-content-between mb-3">
              <span className="small">Modo oscuro</span>
              <button
                className="btn btn-sm btn-outline-secondary"
                onClick={toggleMode}
              >
                {theme.mode === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
              </button>
            </div>

            {/* Selector de color */}
            <div className="mb-3">
              <label className="form-label small">Color del tema</label>
              <div className="d-flex gap-2 flex-wrap">
                {colorOptions.map((color) => (
                  <button
                    key={color.value}
                    className={`btn btn-sm ${color.class} ${theme.color === color.value ? 'border border-dark' : ''}`}
                    style={{ width: '32px', height: '32px' }}
                    onClick={() => setColor(color.value as any)}
                    title={color.label}
                  />
                ))}
              </div>
            </div>

            {/* Botón de logout */}
            <button
              className="btn btn-outline-danger btn-sm w-100"
              onClick={handleLogout}
            >
              <LogOut size={16} className="me-2" />
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

export default Sidebar 