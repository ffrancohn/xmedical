import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '@/contexts/AuthContext'
import { 
  FileText, 
  MapPin, 
  Users, 
  MessageSquare, 
  CheckCircle, 
  AlertTriangle,
  TrendingUp,
  Activity,
  Calendar,
  Clock
} from 'lucide-react'
import { documentService, addressService, beneficiaryService, feedbackService } from '@/services/api'

const Dashboard: React.FC = () => {
  const { user } = useAuth()

  // Consultas para obtener datos del dashboard
  const { data: documents, isLoading: loadingDocuments } = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.getDocuments
  })

  const { data: addresses, isLoading: loadingAddresses } = useQuery({
    queryKey: ['addresses'],
    queryFn: addressService.getAddresses
  })

  const { data: beneficiaries, isLoading: loadingBeneficiaries } = useQuery({
    queryKey: ['beneficiaries'],
    queryFn: beneficiaryService.getBeneficiaries
  })

  const { data: feedback, isLoading: loadingFeedback } = useQuery({
    queryKey: ['feedback'],
    queryFn: feedbackService.getFeedback
  })

  // Calcular estadísticas
  const stats = {
    documents: {
      total: documents?.length || 0,
      valid: documents?.filter(d => d.isValid).length || 0,
      pending: documents?.filter(d => !d.isValid).length || 0
    },
    addresses: addresses?.length || 0,
    beneficiaries: beneficiaries?.length || 0,
    feedback: {
      total: feedback?.length || 0,
      pending: feedback?.filter(f => f.status === 'pending').length || 0,
      resolved: feedback?.filter(f => f.status === 'resolved').length || 0
    }
  }

  const isLoading = loadingDocuments || loadingAddresses || loadingBeneficiaries || loadingFeedback

  if (isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="text-center">
          <div className="loading-spinner mb-3"></div>
          <p className="text-muted">Cargando dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      {/* Header del dashboard */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h3 mb-1">Dashboard</h1>
          <p className="text-muted mb-0">
            Bienvenido de vuelta, {user?.fullName}
          </p>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-primary btn-sm">
            <Calendar size={16} className="me-1" />
            Hoy
          </button>
          <button className="btn btn-outline-secondary btn-sm">
            <Clock size={16} className="me-1" />
            Última semana
          </button>
        </div>
      </div>

      {/* Tarjetas de estadísticas */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <div className="card card-hover h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="bg-primary bg-opacity-10 rounded p-3 me-3">
                  <FileText size={24} className="text-primary" />
                </div>
                <div>
                  <h6 className="card-title mb-1">Documentos</h6>
                  <h3 className="mb-0">{stats.documents.total}</h3>
                  <small className="text-muted">
                    {stats.documents.valid} verificados
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card card-hover h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="bg-success bg-opacity-10 rounded p-3 me-3">
                  <MapPin size={24} className="text-success" />
                </div>
                <div>
                  <h6 className="card-title mb-1">Direcciones</h6>
                  <h3 className="mb-0">{stats.addresses}</h3>
                  <small className="text-muted">
                    Registradas
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card card-hover h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="bg-warning bg-opacity-10 rounded p-3 me-3">
                  <Users size={24} className="text-warning" />
                </div>
                <div>
                  <h6 className="card-title mb-1">Beneficiarios</h6>
                  <h3 className="mb-0">{stats.beneficiaries}</h3>
                  <small className="text-muted">
                    Registrados
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card card-hover h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="bg-info bg-opacity-10 rounded p-3 me-3">
                  <MessageSquare size={24} className="text-info" />
                </div>
                <div>
                  <h6 className="card-title mb-1">Feedback</h6>
                  <h3 className="mb-0">{stats.feedback.total}</h3>
                  <small className="text-muted">
                    {stats.feedback.pending} pendientes
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="row">
        {/* Documentos recientes */}
        <div className="col-md-6 mb-4">
          <div className="card h-100">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Documentos Recientes</h5>
              <a href="/documents" className="btn btn-sm btn-outline-primary">
                Ver todos
              </a>
            </div>
            <div className="card-body">
              {documents && documents.length > 0 ? (
                <div className="list-group list-group-flush">
                  {documents.slice(0, 5).map((doc) => (
                    <div key={doc.id} className="list-group-item d-flex justify-content-between align-items-center border-0 px-0">
                      <div>
                        <h6 className="mb-1">{doc.documentType}</h6>
                        <small className="text-muted">{doc.documentNumber}</small>
                      </div>
                      <span className={`badge ${doc.isValid ? 'bg-success' : 'bg-warning'}`}>
                        {doc.isValid ? 'Válido' : 'Pendiente'}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted text-center py-3">
                  No hay documentos registrados
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Feedback reciente */}
        <div className="col-md-6 mb-4">
          <div className="card h-100">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Feedback Reciente</h5>
              <a href="/feedback" className="btn btn-sm btn-outline-primary">
                Ver todos
              </a>
            </div>
            <div className="card-body">
              {feedback && feedback.length > 0 ? (
                <div className="list-group list-group-flush">
                  {feedback.slice(0, 5).map((item) => (
                    <div key={item.id} className="list-group-item border-0 px-0">
                      <div className="d-flex justify-content-between align-items-start">
                        <div className="flex-grow-1">
                          <h6 className="mb-1">{item.subject}</h6>
                          <p className="mb-1 small text-muted">{item.message.substring(0, 60)}...</p>
                          <small className="text-muted">{item.type} • {item.priority}</small>
                        </div>
                        <span className={`badge ${item.status === 'resolved' ? 'bg-success' : 'bg-warning'}`}>
                          {item.status === 'resolved' ? 'Resuelto' : 'Pendiente'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted text-center py-3">
                  No hay feedback registrado
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Acciones rápidas */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Acciones Rápidas</h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-3 mb-3">
                  <a href="/documents" className="btn btn-outline-primary w-100 h-100 d-flex flex-column align-items-center justify-content-center p-3">
                    <FileText size={32} className="mb-2" />
                    <span>Agregar Documento</span>
                  </a>
                </div>
                <div className="col-md-3 mb-3">
                  <a href="/addresses" className="btn btn-outline-success w-100 h-100 d-flex flex-column align-items-center justify-content-center p-3">
                    <MapPin size={32} className="mb-2" />
                    <span>Registrar Dirección</span>
                  </a>
                </div>
                <div className="col-md-3 mb-3">
                  <a href="/beneficiaries" className="btn btn-outline-warning w-100 h-100 d-flex flex-column align-items-center justify-content-center p-3">
                    <Users size={32} className="mb-2" />
                    <span>Agregar Beneficiario</span>
                  </a>
                </div>
                <div className="col-md-3 mb-3">
                  <a href="/feedback" className="btn btn-outline-info w-100 h-100 d-flex flex-column align-items-center justify-content-center p-3">
                    <MessageSquare size={32} className="mb-2" />
                    <span>Enviar Feedback</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Estado del sistema */}
      <div className="row mt-4">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Estado del Sistema</h5>
            </div>
            <div className="card-body">
              <div className="d-flex align-items-center mb-3">
                <CheckCircle size={20} className="text-success me-2" />
                <span>Sistema operativo</span>
              </div>
              <div className="d-flex align-items-center mb-3">
                <CheckCircle size={20} className="text-success me-2" />
                <span>Base de datos conectada</span>
              </div>
              <div className="d-flex align-items-center mb-3">
                <CheckCircle size={20} className="text-success me-2" />
                <span>Servicios biométricos activos</span>
              </div>
              <div className="d-flex align-items-center">
                <Activity size={20} className="text-info me-2" />
                <span>Última actualización: hace 5 minutos</span>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Actividad Reciente</h5>
            </div>
            <div className="card-body">
              <div className="timeline">
                <div className="timeline-item mb-3">
                  <div className="d-flex">
                    <div className="bg-primary rounded-circle me-3" style={{ width: '8px', height: '8px', marginTop: '6px' }}></div>
                    <div>
                      <small className="text-muted">Hace 2 horas</small>
                      <p className="mb-0 small">Documento de identidad verificado</p>
                    </div>
                  </div>
                </div>
                <div className="timeline-item mb-3">
                  <div className="d-flex">
                    <div className="bg-success rounded-circle me-3" style={{ width: '8px', height: '8px', marginTop: '6px' }}></div>
                    <div>
                      <small className="text-muted">Hace 4 horas</small>
                      <p className="mb-0 small">Nuevo beneficiario agregado</p>
                    </div>
                  </div>
                </div>
                <div className="timeline-item">
                  <div className="d-flex">
                    <div className="bg-warning rounded-circle me-3" style={{ width: '8px', height: '8px', marginTop: '6px' }}></div>
                    <div>
                      <small className="text-muted">Hace 1 día</small>
                      <p className="mb-0 small">Feedback enviado</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard 