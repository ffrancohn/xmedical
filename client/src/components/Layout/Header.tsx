import React from 'react'
import { useLocation } from 'wouter'
import { useAuth } from '@/contexts/AuthContext'
import { 
  Bell, 
  Search, 
  Menu,
  Home,
  User,
  FileText,
  MapPin,
  Users,
  MessageSquare,
  Settings
} from 'lucide-react'

interface HeaderProps {
  onMenuToggle: () => void
}

const Header: React.FC<HeaderProps> = ({ onMenuToggle }) => {
  const { user } = useAuth()
  const [location] = useLocation()

  const getBreadcrumbItems = () => {
    const pathMap: { [key: string]: { label: string; icon: React.ComponentType<any> } } = {
      '/dashboard': { label: 'Dashboard', icon: Home },
      '/profile': { label: 'Perfil', icon: User },
      '/documents': { label: 'Documentos', icon: FileText },
      '/addresses': { label: 'Direcciones', icon: MapPin },
      '/beneficiaries': { label: 'Beneficiarios', icon: Users },
      '/feedback': { label: 'Feedback', icon: MessageSquare },
      '/admin': { label: 'Administración', icon: Settings }
    }

    const currentPath = pathMap[location]
    if (!currentPath) return []

    return [
      { label: 'Inicio', path: '/dashboard' },
      { label: currentPath.label, path: location, current: true }
    ]
  }

  const breadcrumbItems = getBreadcrumbItems()

  return (
    <header className="header">
      <div className="container-fluid">
        <div className="row align-items-center">
          {/* Botón de menú y breadcrumbs */}
          <div className="col-md-6">
            <div className="d-flex align-items-center">
              <button
                className="btn btn-link d-md-none me-3"
                onClick={onMenuToggle}
              >
                <Menu size={24} />
              </button>
              
              <nav aria-label="breadcrumb">
                <ol className="breadcrumb mb-0">
                  {breadcrumbItems.map((item, index) => (
                    <li 
                      key={index} 
                      className={`breadcrumb-item ${item.current ? 'active' : ''}`}
                    >
                      {item.current ? (
                        <span>{item.label}</span>
                      ) : (
                        <a href={item.path} className="text-decoration-none">
                          {item.label}
                        </a>
                      )}
                    </li>
                  ))}
                </ol>
              </nav>
            </div>
          </div>

          {/* Acciones del header */}
          <div className="col-md-6">
            <div className="d-flex align-items-center justify-content-end gap-3">
              {/* Barra de búsqueda */}
              <div className="position-relative d-none d-md-block">
                <input
                  type="text"
                  className="form-control form-control-sm"
                  placeholder="Buscar..."
                  style={{ width: '250px' }}
                />
                <Search 
                  size={16} 
                  className="position-absolute top-50 end-0 translate-middle-y me-2 text-muted"
                />
              </div>

              {/* Notificaciones */}
              <div className="dropdown">
                <button
                  className="btn btn-link position-relative"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <Bell size={20} />
                  <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                    3
                  </span>
                </button>
                <ul className="dropdown-menu dropdown-menu-end">
                  <li><h6 className="dropdown-header">Notificaciones</h6></li>
                  <li><a className="dropdown-item" href="#">Documento verificado exitosamente</a></li>
                  <li><a className="dropdown-item" href="#">Nuevo beneficiario agregado</a></li>
                  <li><a className="dropdown-item" href="#">Respuesta a tu feedback</a></li>
                  <li><hr className="dropdown-divider" /></li>
                  <li><a className="dropdown-item" href="#">Ver todas</a></li>
                </ul>
              </div>

              {/* Información del usuario */}
              {user && (
                <div className="dropdown">
                  <button
                    className="btn btn-link d-flex align-items-center gap-2"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    <div className="bg-primary rounded-circle d-flex align-items-center justify-content-center" style={{ width: '32px', height: '32px' }}>
                      <span className="text-white fw-bold">
                        {user.fullName.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <span className="d-none d-md-block">{user.fullName}</span>
                  </button>
                  <ul className="dropdown-menu dropdown-menu-end">
                    <li><a className="dropdown-item" href="/profile">Mi perfil</a></li>
                    <li><a className="dropdown-item" href="/settings">Configuración</a></li>
                    <li><hr className="dropdown-divider" /></li>
                    <li><a className="dropdown-item" href="#" onClick={() => window.location.href = '/login'}>Cerrar sesión</a></li>
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header 