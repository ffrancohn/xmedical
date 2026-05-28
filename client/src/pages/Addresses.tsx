import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/contexts/AuthContext'
import { addressService } from '@/services/api'
import { MapPin, Plus, Edit, Trash2, Search } from 'lucide-react'

const addressSchema = z.object({
  country: z.string().min(1, 'El país es requerido'),
  state: z.string().min(1, 'El estado es requerido'),
  city: z.string().min(1, 'La ciudad es requerida'),
  fullAddress: z.string().min(1, 'La dirección es requerida'),
  zipCode: z.string().optional(),
  exteriorNumber: z.string().optional(),
  interiorNumber: z.string().optional()
})

type AddressFormData = z.infer<typeof addressSchema>

const Addresses: React.FC = () => {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [showModal, setShowModal] = useState(false)
  const [editingAddress, setEditingAddress] = useState<any>(null)

  const { data: addresses, isLoading } = useQuery({
    queryKey: ['addresses'],
    queryFn: addressService.getAddresses
  })

  const createMutation = useMutation({
    mutationFn: addressService.createAddress,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['addresses'] })
      setShowModal(false)
      reset()
    }
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      addressService.updateAddress(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['addresses'] })
      setShowModal(false)
      setEditingAddress(null)
      reset()
    }
  })

  const deleteMutation = useMutation({
    mutationFn: addressService.deleteAddress,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['addresses'] })
    }
  })

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<AddressFormData>({
    resolver: zodResolver(addressSchema)
  })

  const onSubmit = async (data: AddressFormData) => {
    try {
      if (editingAddress) {
        await updateMutation.mutateAsync({ id: editingAddress.id, data })
      } else {
        await createMutation.mutateAsync({ ...data, userId: user?.id })
      }
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const handleEdit = (address: any) => {
    setEditingAddress(address)
    reset(address)
    setShowModal(true)
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta dirección?')) {
      await deleteMutation.mutateAsync(id)
    }
  }

  if (isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="text-center">
          <div className="loading-spinner mb-3"></div>
          <p className="text-muted">Cargando direcciones...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="addresses-page">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h3 mb-1">Direcciones</h1>
          <p className="text-muted mb-0">Gestiona tus direcciones registradas</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} className="me-2" />
          Agregar dirección
        </button>
      </div>

      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Lista de Direcciones</h5>
        </div>
        <div className="card-body">
          {addresses && addresses.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>País</th>
                    <th>Estado</th>
                    <th>Ciudad</th>
                    <th>Dirección</th>
                    <th>Código Postal</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {addresses.map((address) => (
                    <tr key={address.id}>
                      <td>{address.country}</td>
                      <td>{address.state}</td>
                      <td>{address.city}</td>
                      <td>{address.fullAddress}</td>
                      <td>{address.zipCode || 'N/A'}</td>
                      <td>
                        <div className="btn-group btn-group-sm">
                          <button 
                            className="btn btn-outline-primary"
                            onClick={() => handleEdit(address)}
                          >
                            <Edit size={14} />
                          </button>
                          <button 
                            className="btn btn-outline-danger"
                            onClick={() => handleDelete(address.id)}
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
              <MapPin size={48} className="text-muted mb-3" />
              <h5>No hay direcciones</h5>
              <p className="text-muted">Agrega tu primera dirección para comenzar</p>
              <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                <Plus size={16} className="me-2" />
                Agregar dirección
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
                  {editingAddress ? 'Editar Dirección' : 'Agregar Dirección'}
                </h5>
                <button 
                  type="button" 
                  className="btn-close"
                  onClick={() => {
                    setShowModal(false)
                    setEditingAddress(null)
                    reset()
                  }}
                />
              </div>
              <form onSubmit={handleSubmit(onSubmit)}>
                <div className="modal-body">
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="country" className="form-label">País *</label>
                      <input
                        type="text"
                        id="country"
                        className={`form-control ${errors.country ? 'is-invalid' : ''}`}
                        {...register('country')}
                      />
                      {errors.country && (
                        <div className="invalid-feedback">{errors.country.message}</div>
                      )}
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="state" className="form-label">Estado *</label>
                      <input
                        type="text"
                        id="state"
                        className={`form-control ${errors.state ? 'is-invalid' : ''}`}
                        {...register('state')}
                      />
                      {errors.state && (
                        <div className="invalid-feedback">{errors.state.message}</div>
                      )}
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="city" className="form-label">Ciudad *</label>
                      <input
                        type="text"
                        id="city"
                        className={`form-control ${errors.city ? 'is-invalid' : ''}`}
                        {...register('city')}
                      />
                      {errors.city && (
                        <div className="invalid-feedback">{errors.city.message}</div>
                      )}
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="zipCode" className="form-label">Código Postal</label>
                      <input
                        type="text"
                        id="zipCode"
                        className="form-control"
                        {...register('zipCode')}
                      />
                    </div>
                    <div className="col-12 mb-3">
                      <label htmlFor="fullAddress" className="form-label">Dirección Completa *</label>
                      <textarea
                        id="fullAddress"
                        className={`form-control ${errors.fullAddress ? 'is-invalid' : ''}`}
                        rows={3}
                        {...register('fullAddress')}
                      />
                      {errors.fullAddress && (
                        <div className="invalid-feedback">{errors.fullAddress.message}</div>
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
                      setEditingAddress(null)
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

export default Addresses 