import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/contexts/AuthContext'
import { feedbackService } from '@/services/api'
import { MessageSquare, Plus, Eye, Send } from 'lucide-react'

const feedbackSchema = z.object({
  type: z.string().min(1, 'Selecciona un tipo'),
  subject: z.string().min(1, 'El asunto es requerido'),
  message: z.string().min(10, 'El mensaje debe tener al menos 10 caracteres'),
  priority: z.string().min(1, 'Selecciona una prioridad')
})

type FeedbackFormData = z.infer<typeof feedbackSchema>

const Feedback: React.FC = () => {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [showModal, setShowModal] = useState(false)
  const [selectedFeedback, setSelectedFeedback] = useState<any>(null)

  const { data: feedback, isLoading } = useQuery({
    queryKey: ['feedback'],
    queryFn: feedbackService.getFeedback
  })

  const createMutation = useMutation({
    mutationFn: feedbackService.createFeedback,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['feedback'] })
      setShowModal(false)
      reset()
    }
  })

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<FeedbackFormData>({
    resolver: zodResolver(feedbackSchema)
  })

  const onSubmit = async (data: FeedbackFormData) => {
    try {
      await createMutation.mutateAsync({ ...data, userId: user?.id, status: 'pending' })
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-danger'
      case 'medium': return 'bg-warning'
      case 'low': return 'bg-info'
      default: return 'bg-secondary'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'resolved': return 'bg-success'
      case 'pending': return 'bg-warning'
      case 'in_progress': return 'bg-info'
      default: return 'bg-secondary'
    }
  }

  if (isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="text-center">
          <div className="loading-spinner mb-3"></div>
          <p className="text-muted">Cargando feedback...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="feedback-page">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h3 mb-1">Feedback</h1>
          <p className="text-muted mb-0">Envía tus comentarios y sugerencias</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} className="me-2" />
          Enviar feedback
        </button>
      </div>

      <div className="row">
        <div className="col-md-8">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Mi Feedback</h5>
            </div>
            <div className="card-body">
              {feedback && feedback.length > 0 ? (
                <div className="list-group list-group-flush">
                  {feedback.map((item) => (
                    <div key={item.id} className="list-group-item border-0 px-0">
                      <div className="d-flex justify-content-between align-items-start">
                        <div className="flex-grow-1">
                          <h6 className="mb-1">{item.subject}</h6>
                          <p className="mb-1 small text-muted">{item.message.substring(0, 100)}...</p>
                          <div className="d-flex gap-2">
                            <span className={`badge ${getPriorityColor(item.priority)}`}>
                              {item.priority}
                            </span>
                            <span className={`badge ${getStatusColor(item.status)}`}>
                              {item.status}
                            </span>
                            <small className="text-muted">{item.type}</small>
                          </div>
                        </div>
                        <button
                          className="btn btn-sm btn-outline-primary"
                          onClick={() => setSelectedFeedback(item)}
                        >
                          <Eye size={14} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-5">
                  <MessageSquare size={48} className="text-muted mb-3" />
                  <h5>No hay feedback</h5>
                  <p className="text-muted">Envía tu primer comentario para comenzar</p>
                  <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                    <Plus size={16} className="me-2" />
                    Enviar feedback
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card">
            <div className="card-header">
              <h6 className="mb-0">Estadísticas</h6>
            </div>
            <div className="card-body">
              <div className="d-flex justify-content-between mb-2">
                <span>Total enviados:</span>
                <span className="fw-bold">{feedback?.length || 0}</span>
              </div>
              <div className="d-flex justify-content-between mb-2">
                <span>Pendientes:</span>
                <span className="fw-bold text-warning">
                  {feedback?.filter(f => f.status === 'pending').length || 0}
                </span>
              </div>
              <div className="d-flex justify-content-between">
                <span>Resueltos:</span>
                <span className="fw-bold text-success">
                  {feedback?.filter(f => f.status === 'resolved').length || 0}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de envío */}
      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Enviar Feedback</h5>
                <button 
                  type="button" 
                  className="btn-close"
                  onClick={() => {
                    setShowModal(false)
                    reset()
                  }}
                />
              </div>
              <form onSubmit={handleSubmit(onSubmit)}>
                <div className="modal-body">
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="type" className="form-label">Tipo *</label>
                      <select 
                        id="type"
                        className={`form-select ${errors.type ? 'is-invalid' : ''}`}
                        {...register('type')}
                      >
                        <option value="">Selecciona...</option>
                        <option value="bug">Error/Bug</option>
                        <option value="feature">Nueva funcionalidad</option>
                        <option value="improvement">Mejora</option>
                        <option value="question">Pregunta</option>
                        <option value="other">Otro</option>
                      </select>
                      {errors.type && (
                        <div className="invalid-feedback">{errors.type.message}</div>
                      )}
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="priority" className="form-label">Prioridad *</label>
                      <select 
                        id="priority"
                        className={`form-select ${errors.priority ? 'is-invalid' : ''}`}
                        {...register('priority')}
                      >
                        <option value="">Selecciona...</option>
                        <option value="low">Baja</option>
                        <option value="medium">Media</option>
                        <option value="high">Alta</option>
                      </select>
                      {errors.priority && (
                        <div className="invalid-feedback">{errors.priority.message}</div>
                      )}
                    </div>
                    <div className="col-12 mb-3">
                      <label htmlFor="subject" className="form-label">Asunto *</label>
                      <input
                        type="text"
                        id="subject"
                        className={`form-control ${errors.subject ? 'is-invalid' : ''}`}
                        placeholder="Resumen del feedback"
                        {...register('subject')}
                      />
                      {errors.subject && (
                        <div className="invalid-feedback">{errors.subject.message}</div>
                      )}
                    </div>
                    <div className="col-12 mb-3">
                      <label htmlFor="message" className="form-label">Mensaje *</label>
                      <textarea
                        id="message"
                        className={`form-control ${errors.message ? 'is-invalid' : ''}`}
                        rows={4}
                        placeholder="Describe detalladamente tu feedback..."
                        {...register('message')}
                      />
                      {errors.message && (
                        <div className="invalid-feedback">{errors.message.message}</div>
                      )}
                    </div>
                  </div>
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => {
                      setShowModal(false)
                      reset()
                    }}
                  >
                    Cancelar
                  </button>
                  <button type="submit" className="btn btn-primary">
                    <Send size={16} className="me-2" />
                    Enviar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Modal de detalle */}
      {selectedFeedback && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Detalle del Feedback</h5>
                <button 
                  type="button" 
                  className="btn-close"
                  onClick={() => setSelectedFeedback(null)}
                />
              </div>
              <div className="modal-body">
                <h6>{selectedFeedback.subject}</h6>
                <p>{selectedFeedback.message}</p>
                <div className="d-flex gap-2 mb-3">
                  <span className={`badge ${getPriorityColor(selectedFeedback.priority)}`}>
                    {selectedFeedback.priority}
                  </span>
                  <span className={`badge ${getStatusColor(selectedFeedback.status)}`}>
                    {selectedFeedback.status}
                  </span>
                  <span className="badge bg-secondary">{selectedFeedback.type}</span>
                </div>
                {selectedFeedback.response && (
                  <div className="alert alert-info">
                    <strong>Respuesta:</strong><br />
                    {selectedFeedback.response}
                  </div>
                )}
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setSelectedFeedback(null)}
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Feedback 