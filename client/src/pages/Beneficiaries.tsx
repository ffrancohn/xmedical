import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/contexts/AuthContext'
import { beneficiaryService } from '@/services/api'
import { Users, Plus, Edit, Trash2 } from 'lucide-react'

const beneficiarySchema = z.object({
  fullName: z.string().min(1, 'El nombre completo es requerido'),
  documentNumber: z.string().min(1, 'El número de documento es requerido'),
  relationship: z.string().min(1, 'La relación es requerida'),
  birthDate: z.string().optional()
})

type BeneficiaryFormData = z.infer<typeof beneficiarySchema>

const Beneficiaries: React.FC = () => {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [showModal, setShowModal] = useState(false)
  const [editingBeneficiary, setEditingBeneficiary] = useState<any>(null)

  const { data: beneficiaries, isLoading } = useQuery({
    queryKey: ['beneficiaries'],
    queryFn: beneficiaryService.getBeneficiaries
  })

  const createMutation = useMutation({
    mutationFn: beneficiaryService.createBeneficiary,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['beneficiaries'] })
      setShowModal(false)
      reset()
    }
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      beneficiaryService.updateBeneficiary(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['beneficiaries'] })
      setShowModal(false)
      setEditingBeneficiary(null)
      reset()
    }
  })

  const deleteMutation = useMutation({
    mutationFn: beneficiaryService.deleteBeneficiary,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['beneficiaries'] })
    }
  })

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<BeneficiaryFormData>({
    resolver: zodResolver(beneficiarySchema)
  })

  const onSubmit = async (data: BeneficiaryFormData) => {
    try {
      if (editingBeneficiary) {
        await updateMutation.mutateAsync({ id: editingBeneficiary.id, data })
      } else {
        await createMutation.mutateAsync({ ...data, userId: user?.id })
      }
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const handleEdit = (beneficiary: any) => {
    setEditingBeneficiary(beneficiary)
    reset(beneficiary)
    setShowModal(true)
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este beneficiario?')) {
      await deleteMutation.mutateAsync(id)
    }
  }

  if (isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="text-center">
          <div className="loading-spinner mb-3"></div>
          <p className="text-muted">Cargando beneficiarios...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="beneficiaries-page">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h3 mb-1">Beneficiarios</h1>
          <p className="text-muted mb-0">Gestiona tus beneficiarios registrados</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} className="me-2" />
          Agregar beneficiario
        </button>
      </div>

      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Lista de Beneficiarios</h5>
        </div>
        <div className="card-body">
          {beneficiaries && beneficiaries.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Nombre Completo</th>
                    <th>Número de Documento</th>
                    <th>Relación</th>
                    <th>Fecha de Nacimiento</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {beneficiaries.map((beneficiary) => (
                    <tr key={beneficiary.id}>
                      <td>{beneficiary.fullName}</td>
                      <td>{beneficiary.documentNumber}</td>
                      <td>{beneficiary.relationship}</td>
                      <td>
                        {beneficiary.birthDate ? new Date(beneficiary.birthDate).toLocaleDateString() : 'N/A'}
                      </td>
                      <td>
                        <div className="btn-group btn-group-sm">
                          <button 
                            className="btn btn-outline-primary"
                            onClick={() => handleEdit(beneficiary)}
                          >
                            <Edit size={14} />
                          </button>
                          <button 
                            className="btn btn-outline-danger"
                            onClick={() => handleDelete(beneficiary.id)}
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-5">
              <Users size={48} className="text-muted mb-3" />
              <h5>No hay beneficiarios</h5>
              <p className="text-muted">Agrega tu primer beneficiario para comenzar</p>
              <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                <Plus size={16} className="me-2" />
                Agregar beneficiario
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  {editingBeneficiary ? 'Editar Beneficiario' : 'Agregar Beneficiario'}
                </h5>
                <button 
                  type="button" 
                  className="btn-close"
                  onClick={() => {
                    setShowModal(false)
                    setEditingBeneficiary(null)
                    reset()
                  }}
                />
              </div>
              <form onSubmit={handleSubmit(onSubmit)}>
                <div className="modal-body">
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="fullName" className="form-label">Nombre Completo *</label>
                      <input
                        type="text"
                        id="fullName"
                        className={`form-control ${errors.fullName ? 'is-invalid' : ''}`}
                        {...register('fullName')}
                      />
                      {errors.fullName && (
                        <div className="invalid-feedback">{errors.fullName.message}</div>
                      )}
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="documentNumber" className="form-label">Número de Documento *</label>
                      <input
                        type="text"
                        id="documentNumber"
                        className={`form-control ${errors.documentNumber ? 'is-invalid' : ''}`}
                        {...register('documentNumber')}
                      />
                      {errors.documentNumber && (
                        <div className="invalid-feedback">{errors.documentNumber.message}</div>
                      )}
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="relationship" className="form-label">Relación *</label>
                      <select 
                        id="relationship"
                        className={`form-select ${errors.relationship ? 'is-invalid' : ''}`}
                        {...register('relationship')}
                      >
                        <option value="">Selecciona...</option>
                        <option value="Cónyuge">Cónyuge</option>
                        <option value="Hijo/a">Hijo/a</option>
                        <option value="Padre">Padre</option>
                        <option value="Madre">Madre</option>
                        <option value="Hermano/a">Hermano/a</option>
                        <option value="Otro">Otro</option>
                      </select>
                      {errors.relationship && (
                        <div className="invalid-feedback">{errors.relationship.message}</div>
                      )}
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="birthDate" className="form-label">Fecha de Nacimiento</label>
                      <input
                        type="date"
                        id="birthDate"
                        className="form-control"
                        {...register('birthDate')}
                      />
                    </div>
                  </div>
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => {
                      setShowModal(false)
                      setEditingBeneficiary(null)
                      reset()
                    }}
                  >
                    Cancelar
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Guardar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Beneficiaries 