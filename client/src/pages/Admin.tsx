import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { userService } from '@/services/api'
import { 
  Users, 
  FileText, 
  MapPin, 
  MessageSquare, 
  Settings, 
  Activity,
  TrendingUp,
  Shield,
  Database
} from 'lucide-react'

const Admin: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard')

  const { data: users, isLoading: loadingUsers } = useQuery({
    queryKey: ['users'],
    queryFn: userService.getUsers
  })

  const stats = {
    totalUsers: users?.length || 0,
    activeUsers: users?.filter(u => u.isActive).length || 0,
    adminUsers: users?.filter(u => u.profileId === 1).length || 0,
    regularUsers: users?.filter(u => u.profileId === 2).length || 0
  }

  if (loadingUsers) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="text-center">
          <div className="loading-spinner mb-3"></div>
          <p className="text-muted">Cargando panel de administración...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="admin-page">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h3 mb-1">Panel de Administración</h1>
          <p className="text-muted mb-0">Gestiona el sistema XMedical</p>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-primary btn-sm">
            <Activity size={16} className="me-1" />
            Logs del sistema
          </button>
          <button className="btn btn-outline-secondary btn-sm">
            <Settings size={16} className="me-1" />
            Configuración
          </button>
        </div>
      </div>

      {/* Estadísticas principales */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <div className="bg-primary bg-opacity-10 rounded p-3 mb-3 mx-auto" style={{ width: 'fit-content' }}>
                <Users size={24} className="text-primary" />
              </div>
              <h3 className="text-primary">{stats.totalUsers}</h3>
              <p className="mb-0">Total Usuarios</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <div className="bg-success bg-opacity-10 rounded p-3 mb-3 mx-auto" style={{ width: 'fit-content' }}>
                <Shield size={24} className="text-success" />
              </div>
              <h3 className="text-success">{stats.activeUsers}</h3>
              <p className="mb-0">Usuarios Activos</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <div className="bg-warning bg-opacity-10 rounded p-3 mb-3 mx-auto" style={{ width: 'fit-content' }}>
                <Database size={24} className="text-warning" />
              </div>
              <h3 className="text-warning">{stats.adminUsers}</h3>
              <p className="mb-0">Administradores</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <div className="bg-info bg-opacity-10 rounded p-3 mb-3 mx-auto" style={{ width: 'fit-content' }}>
                <TrendingUp size={24} className="text-info" />
              </div>
              <h3 className="text-info">{stats.regularUsers}</h3>
              <p className="mb-0">Usuarios Regulares</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs de navegación */}
      <div className="card">
        <div className="card-header">
          <ul className="nav nav-tabs card-header-tabs">
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}
                onClick={() => setActiveTab('dashboard')}
              >
                Dashboard
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === 'users' ? 'active' : ''}`}
                onClick={() => setActiveTab('users')}
              >
                Usuarios
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === 'system' ? 'active' : ''}`}
                onClick={() => setActiveTab('system')}
              >
                Sistema
              </button>
            </li>
          </ul>
        </div>
        <div className="card-body">
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && (
            <div className="row">
              <div className="col-md-8">
                <h5>Actividad Reciente</h5>
                <div className="list-group list-group-flush">
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                      <h6 className="mb-1">Nuevo usuario registrado</h6>
                      <small className="text-muted">Juan Pérez se registró en el sistema</small>
                    </div>
                    <small className="text-muted">Hace 2 horas</small>
                  </div>
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                      <h6 className="mb-1">Documento verificado</h6>
                      <small className="text-muted">DNI de María García fue verificado exitosamente</small>
                    </div>
                    <small className="text-muted">Hace 4 horas</small>
                  </div>
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                      <h6 className="mb-1">Feedback enviado</h6>
                      <small className="text-muted">Nuevo feedback sobre la interfaz de usuario</small>
                    </div>
                    <small className="text-muted">Hace 6 horas</small>
                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <h5>Estado del Sistema</h5>
                <div className="list-group list-group-flush">
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <span>API Backend</span>
                    <span className="badge bg-success">Operativo</span>
                  </div>
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <span>Base de Datos</span>
                    <span className="badge bg-success">Conectada</span>
                  </div>
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <span>Servicios OCR</span>
                    <span className="badge bg-success">Activo</span>
                  </div>
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <span>Verificación Facial</span>
                    <span className="badge bg-success">Disponible</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Users Tab */}
          {activeTab === 'users' && (
            <div>
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h5>Gestión de Usuarios</h5>
                <button className="btn btn-primary btn-sm">
                  <Users size={16} className="me-1" />
                  Agregar Usuario
                </button>
              </div>
              <div className="table-responsive">
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nombre</th>
                      <th>Email</th>
                      <th>Usuario</th>
                      <th>Perfil</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users?.map((user) => (
                      <tr key={user.id}>
                        <td>{user.id}</td>
                        <td>{user.fullName}</td>
                        <td>{user.email}</td>
                        <td>{user.username}</td>
                        <td>
                          <span className={`badge ${user.profileId === 1 ? 'bg-danger' : 'bg-primary'}`}>
                            {user.profileId === 1 ? 'Admin' : 'Usuario'}
                          </span>
                        </td>
                        <td>
                          <span className={`badge ${user.isActive ? 'bg-success' : 'bg-danger'}`}>
                            {user.isActive ? 'Activo' : 'Inactivo'}
                          </span>
                        </td>
                        <td>
                          <div className="btn-group btn-group-sm">
                            <button className="btn btn-outline-primary">
                              <Settings size={14} />
                            </button>
                            <button className="btn btn-outline-warning">
                              <Shield size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* System Tab */}
          {activeTab === 'system' && (
            <div className="row">
              <div className="col-md-6">
                <h5>Configuración del Sistema</h5>
                <div className="list-group list-group-flush">
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <span>Modo de mantenimiento</span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" />
                    </div>
                  </div>
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <span>Registro de usuarios</span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" defaultChecked />
                    </div>
                  </div>
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <span>Verificación automática</span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" defaultChecked />
                    </div>
                  </div>
                  <div className="list-group-item d-flex justify-content-between align-items-center">
                    <span>Notificaciones por email</span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" defaultChecked />
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-md-6">
                <h5>Información del Sistema</h5>
                <div className="list-group list-group-flush">
                  <div className="list-group-item d-flex justify-content-between">
                    <span>Versión</span>
                    <span>1.0.0</span>
                  </div>
                  <div className="list-group-item d-flex justify-content-between">
                    <span>Última actualización</span>
                    <span>2024-01-15</span>
                  </div>
                  <div className="list-group-item d-flex justify-content-between">
                    <span>Base de datos</span>
                    <span>PostgreSQL 15</span>
                  </div>
                  <div className="list-group-item d-flex justify-content-between">
                    <span>Servidor</span>
                    <span>FastAPI 0.104.1</span>
                  </div>
                  <div className="list-group-item d-flex justify-content-between">
                    <span>Frontend</span>
                    <span>React 18.2.0</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Admin 