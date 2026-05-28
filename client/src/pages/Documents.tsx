import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/contexts/AuthContext'
import { documentService, uploadService, biometricService } from '@/services/api'
import { 
  FileText, 
  Plus, 
  Edit, 
  Trash2, 
  Eye, 
  Upload, 
  Camera,
  CheckCircle,
  AlertCircle,
  AlertTriangle
} from 'lucide-react'

// Esquema de validación
const documentSchema = z.object({
  documentType: z.string().min(1, 'Selecciona un tipo de documento'),
  documentNumber: z.string().min(1, 'El número de documento es requerido'),
  expiryDate: z.string().optional()
})

type DocumentFormData = z.infer<typeof documentSchema>

const Documents: React.FC = () => {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [showModal, setShowModal] = useState(false)
  const [editingDocument, setEditingDocument] = useState<any>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  // Consultas
  const { data: documents, isLoading } = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.getDocuments
  })

  // Mutaciones
  const createMutation = useMutation({
    mutationFn: documentService.createDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] })
      setShowModal(false)
      reset()
    }
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      documentService.updateDocument(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] })
      setShowModal(false)
      setEditingDocument(null)
      reset()
    }
  })

  const deleteMutation = useMutation({
    mutationFn: documentService.deleteDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] })
    }
  })

  // Formulario
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<DocumentFormData>({
    resolver: zodResolver(documentSchema)
  })

  const onSubmit = async (data: DocumentFormData) => {
    try {
      setIsProcessing(true)
      
      if (editingDocument) {
        await updateMutation.mutateAsync({ id: editingDocument.id, data })
      } else {
        await createMutation.mutateAsync({ ...data, userId: user?.id })
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleEdit = (document: any) => {
    setEditingDocument(document)
    reset({
      documentType: document.documentType,
      documentNumber: document.documentNumber,
      expiryDate: document.expiryDate
    })
    setShowModal(true)
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este documento?')) {
      await deleteMutation.mutateAsync(id)
    }
  }

  const handleFileUpload = async (file: File) => {
    try {
      setIsProcessing(true)
      const result = await uploadService.uploadFile(file)
      
      // Procesar OCR si es una imagen
      if (file.type.startsWith('image/')) {
        const ocrResult = await biometricService.processOCR(result.url)
        console.log('OCR Result:', ocrResult)
      }
      
      setSelectedFile(null)
    } catch (error) {
      console.error('Error uploading file:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  if (isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="text-center">
          <div className="loading-spinner mb-3"></div>
          <p className="text-muted">Cargando documentos...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="documents-page">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h3 mb-1">Documentos</h1>
          <p className="text-muted mb-0">Gestiona tus documentos de identidad</p>
        </div>
        <button 
          className="btn btn-primary"
          onClick={() => setShowModal(true)}
        >
          <Plus size={16} className="me-2" />
          Agregar documento
        </button>
      </div>

      {/* Estadísticas */}
      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-primary">{documents?.length || 0}</h3>
              <p className="mb-0">Total</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-success">
                {documents?.filter(d => d.isValid).length || 0}
              </h3>
              <p className="mb-0">Verificados</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-warning">
                {documents?.filter(d => !d.isValid).length || 0}
              </h3>
              <p className="mb-0">Pendientes</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-info">
                {documents?.filter(d => d.expiryDate && new Date(d.expiryDate) < new Date()).length || 0}
              </h3>
              <p className="mb-0">Expirados</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabla de documentos */}
      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Lista de Documentos</h5>
        </div>
        <div className="card-body">
          {documents && documents.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Tipo</th>
                    <th>Número</th>
                    <th>Fecha de vencimiento</th>
                    <th>Estado</th>
                    <th>OCR</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.map((doc) => (
                    <tr key={doc.id}>
                      <td>{doc.documentType}</td>
                      <td>{doc.documentNumber}</td>
                      <td>
                        {doc.expiryDate ? new Date(doc.expiryDate).toLocaleDateString() : 'N/A'}
                      </td>
                      <td>
                        <span className={`badge ${doc.isValid ? 'bg-success' : 'bg-warning'}`}>
                          {doc.isValid ? 'Válido' : 'Pendiente'}
                        </span>
                      </td>
                      <td>
                        {doc.ocrData ? (
                          <CheckCircle size={16} className="text-success" />
                        ) : (
                          <AlertTriangle size={16} className="text-warning" />
                        )}
                      </td>
                      <td>
                        <div className="btn-group btn-group-sm">
                          <button 
                            className="btn btn-outline-primary"
                            onClick={() => handleEdit(doc)}
                          >
                            <Edit size={14} />
                          </button>
                          <button 
                            className="btn btn-outline-danger"
                            onClick={() => handleDelete(doc.id)}
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
              <FileText size={48} className="text-muted mb-3" />
              <h5>No hay documentos</h5>
              <p className="text-muted">Agrega tu primer documento para comenzar</p>
              <button 
                className="btn btn-primary"
                onClick={() => setShowModal(true)}
              >
                <Plus size={16} className="me-2" />
                Agregar documento
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Modal de documento */}
      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-lg">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  {editingDocument ? 'Editar Documento' : 'Agregar Documento'}
                </h5>
                <button 
                  type="button" 
                  className="btn-close"
                  onClick={() => {
                    setShowModal(false)
                    setEditingDocument(null)
                    reset()
                  }}
                />
              </div>
              <form onSubmit={handleSubmit(onSubmit)}>
                <div className="modal-body">
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="documentType" className="form-label">
                        Tipo de documento *
                      </label>
                      <select 
                        id="documentType"
                        className={`form-select ${errors.documentType ? 'is-invalid' : ''}`}
                        {...register('documentType')}
                      >
                        <option value="">Selecciona...</option>
                        <option value="DNI">DNI</option>
                        <option value="Pasaporte">Pasaporte</option>
                        <option value="Licencia">Licencia de conducir</option>
                        <option value="Otro">Otro</option>
                      </select>
                      {errors.documentType && (
                        <div className="invalid-feedback">{errors.documentType.message}</div>
                      )}
                    </div>

                    <div className="col-md-6 mb-3">
                      <label htmlFor="documentNumber" className="form-label">
                        Número de documento *
                      </label>
                      <input
                        type="text"
                        id="documentNumber"
                        className={`form-control ${errors.documentNumber ? 'is-invalid' : ''}`}
                        placeholder="Ingresa el número"
                        {...register('documentNumber')}
                      />
                      {errors.documentNumber && (
                        <div className="invalid-feedback">{errors.documentNumber.message}</div>
                      )}
                    </div>

                    <div className="col-md-6 mb-3">
                      <label htmlFor="expiryDate" className="form-label">
                        Fecha de vencimiento
                      </label>
                      <input
                        type="date"
                        id="expiryDate"
                        className="form-control"
                        {...register('expiryDate')}
                      />
                    </div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label">Subir imagen</label>
                      <div className="d-flex gap-2">
                        <input
                          type="file"
                          className="form-control"
                          accept="image/*"
                          onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                        />
                        {selectedFile && (
                          <button
                            type="button"
                            className="btn btn-outline-primary"
                            onClick={() => handleFileUpload(selectedFile)}
                            disabled={isProcessing}
                          >
                            {isProcessing ? (
                              <div className="loading-spinner"></div>
                            ) : (
                              <Upload size={16} />
                            )}
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => {
                      setShowModal(false)
                      setEditingDocument(null)
                      reset()
                    }}
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={isProcessing}
                  >
                    {isProcessing ? (
                      <>
                        <div className="loading-spinner me-2"></div>
                        Guardando...
                      </>
                    ) : (
                      'Guardar'
                    )}
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

export default Documents 