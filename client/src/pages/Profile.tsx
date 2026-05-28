import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/contexts/AuthContext'
import { useTheme } from '@/contexts/ThemeContext'
import { userService } from '@/services/api'
import { 
  User, 
  Mail, 
  Phone, 
  Calendar, 
  MapPin, 
  Save, 
  Edit, 
  Eye, 
  EyeOff,
  AlertCircle,
  CheckCircle
} from 'lucide-react'

// Esquema de validación
const profileSchema = z.object({
  fullName: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
  email: z.string().email('Ingresa un email válido'),
  phone: z.string().optional(),
  birthDate: z.string().optional(),
  gender: z.string().optional(),
  themeMode: z.string().optional(),
  colorTheme: z.string().optional()
})

type ProfileFormData = z.infer<typeof profileSchema>

const Profile: React.FC = () => {
  const { user, refreshUser } = useAuth()
  const { theme, setTheme } = useTheme()
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      fullName: user?.fullName || '',
      email: user?.email || '',
      phone: user?.phone || '',
      birthDate: user?.birthDate || '',
      gender: user?.gender || '',
      themeMode: theme.mode,
      colorTheme: theme.color
    }
  })

  const onSubmit = async (data: ProfileFormData) => {
    try {
      setIsLoading(true)
      setError('')
      setSuccess('')

      if (user) {
        await userService.updateUser(user.id, data)
        
        // Actualizar tema si cambió
        if (data.themeMode || data.colorTheme) {
          setTheme({
            mode: (data.themeMode as any) || theme.mode,
            color: (data.colorTheme as any) || theme.color
          })
        }

        await refreshUser()
        setSuccess('Perfil actualizado exitosamente')
        setIsEditing(false)
      }
    } catch (err: any) {
      setError(err.message || 'Error al actualizar perfil')
    } finally {
      setIsLoading(false)
    }
  }

  const handleEdit = () => {
    setIsEditing(true)
    reset({
      fullName: user?.fullName || '',
      email: user?.email || '',
      phone: user?.phone || '',
      birthDate: user?.birthDate || '',
      gender: user?.gender || '',
      themeMode: theme.mode,
      colorTheme: theme.color
    })
  }

  const handleCancel = () => {
    setIsEditing(false)
    setError('')
    setSuccess('')
    reset()
  }

  if (!user) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="text-center">
          <div className="loading-spinner mb-3"></div>
          <p className="text-muted">Cargando perfil...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="profile-page">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h3 mb-1">Mi Perfil</h1>
          <p className="text-muted mb-0">Gestiona tu información personal</p>
        </div>
        {!isEditing && (
          <button className="btn btn-primary" onClick={handleEdit}>
            <Edit size={16} className="me-2" />
            Editar perfil
          </button>
        )}
      </div>

      {/* Mensajes de estado */}
      {error && (
        <div className="alert alert-danger d-flex align-items-center mb-3">
          <AlertCircle size={16} className="me-2" />
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success d-flex align-items-center mb-3">
          <CheckCircle size={16} className="me-2" />
          {success}
        </div>
      )}

      <div className="row">
        {/* Información personal */}
        <div className="col-md-8">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Información Personal</h5>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit(onSubmit)}>
                <div className="row">
                  {/* Nombre completo */}
                  <div className="col-md-6 mb-3">
                    <label htmlFor="fullName" className="form-label">
                      Nombre completo *
                    </label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <User size={16} />
                      </span>
                      <input
                        type="text"
                        id="fullName"
                        className={`form-control ${errors.fullName ? 'is-invalid' : ''}`}
                        placeholder="Tu nombre completo"
                        {...register('fullName')}
                        disabled={!isEditing}
                      />
                    </div>
                    {errors.fullName && (
                      <div className="invalid-feedback d-flex align-items-center">
                        <AlertCircle size={16} className="me-1" />
                        {errors.fullName.message}
                      </div>
                    )}
                  </div>

                  {/* Email */}
                  <div className="col-md-6 mb-3">
                    <label htmlFor="email" className="form-label">
                      Email *
                    </label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <Mail size={16} />
                      </span>
                      <input
                        type="email"
                        id="email"
                        className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                        placeholder="tu@email.com"
                        {...register('email')}
                        disabled={!isEditing}
                      />
                    </div>
                    {errors.email && (
                      <div className="invalid-feedback d-flex align-items-center">
                        <AlertCircle size={16} className="me-1" />
                        {errors.email.message}
                      </div>
                    )}
                  </div>

                  {/* Teléfono */}
                  <div className="col-md-6 mb-3">
                    <label htmlFor="phone" className="form-label">
                      Teléfono
                    </label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <Phone size={16} />
                      </span>
                      <input
                        type="tel"
                        id="phone"
                        className="form-control"
                        placeholder="Tu teléfono"
                        {...register('phone')}
                        disabled={!isEditing}
                      />
                    </div>
                  </div>

                  {/* Fecha de nacimiento */}
                  <div className="col-md-6 mb-3">
                    <label htmlFor="birthDate" className="form-label">
                      Fecha de nacimiento
                    </label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <Calendar size={16} />
                      </span>
                      <input
                        type="date"
                        id="birthDate"
                        className="form-control"
                        {...register('birthDate')}
                        disabled={!isEditing}
                      />
                    </div>
                  </div>

                  {/* Género */}
                  <div className="col-md-6 mb-3">
                    <label htmlFor="gender" className="form-label">
                      Género
                    </label>
                    <select 
                      id="gender" 
                      className="form-select"
                      {...register('gender')}
                      disabled={!isEditing}
                    >
                      <option value="">Selecciona...</option>
                      <option value="M">Masculino</option>
                      <option value="F">Femenino</option>
                      <option value="O">Otro</option>
                    </select>
                  </div>

                  {/* Nombre de usuario (solo lectura) */}
                  <div className="col-md-6 mb-3">
                    <label htmlFor="username" className="form-label">
                      Nombre de usuario
                    </label>
                    <input
                      type="text"
                      id="username"
                      className="form-control"
                      value={user.username}
                      disabled
                    />
                    <small className="text-muted">No se puede cambiar</small>
                  </div>
                </div>

                {/* Botones de acción */}
                {isEditing && (
                  <div className="d-flex gap-2 mt-3">
                    <button
                      type="submit"
                      className="btn btn-primary"
                      disabled={isLoading}
                    >
                      {isLoading ? (
                        <>
                          <div className="loading-spinner me-2"></div>
                          Guardando...
                        </>
                      ) : (
                        <>
                          <Save size={16} className="me-2" />
                          Guardar cambios
                        </>
                      )}
                    </button>
                    <button
                      type="button"
                      className="btn btn-outline-secondary"
                      onClick={handleCancel}
                    >
                      Cancelar
                    </button>
                  </div>
                )}
              </form>
            </div>
          </div>
        </div>

        {/* Información adicional */}
        <div className="col-md-4">
          {/* Avatar y información básica */}
          <div className="card mb-3">
            <div className="card-body text-center">
              <div className="bg-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style={{ width: '80px', height: '80px' }}>
                <User size={40} className="text-white" />
              </div>
              <h5 className="mb-1">{user.fullName}</h5>
              <p className="text-muted mb-2">{user.email}</p>
              <span className="badge bg-primary">Usuario Activo</span>
            </div>
          </div>

          {/* Configuración de tema */}
          <div className="card">
            <div className="card-header">
              <h6 className="mb-0">Configuración de Tema</h6>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label className="form-label small">Modo</label>
                <div className="d-flex gap-2">
                  <button
                    className={`btn btn-sm ${theme.mode === 'light' ? 'btn-primary' : 'btn-outline-primary'}`}
                    onClick={() => setTheme({ ...theme, mode: 'light' })}
                    disabled={!isEditing}
                  >
                    Claro
                  </button>
                  <button
                    className={`btn btn-sm ${theme.mode === 'dark' ? 'btn-primary' : 'btn-outline-primary'}`}
                    onClick={() => setTheme({ ...theme, mode: 'dark' })}
                    disabled={!isEditing}
                  >
                    Oscuro
                  </button>
                </div>
              </div>

              <div>
                <label className="form-label small">Color</label>
                <div className="d-flex gap-2 flex-wrap">
                  {['blue', 'green', 'purple', 'orange', 'red', 'slate'].map((color) => (
                    <button
                      key={color}
                      className={`btn btn-sm ${theme.color === color ? 'btn-primary' : 'btn-outline-primary'}`}
                      style={{ width: '32px', height: '32px' }}
                      onClick={() => setTheme({ ...theme, color: color as any })}
                      disabled={!isEditing}
                      title={color}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Información del sistema */}
      <div className="row mt-4">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Información del Sistema</h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-3">
                  <small className="text-muted">ID de Usuario</small>
                  <p className="mb-0">{user.id}</p>
                </div>
                <div className="col-md-3">
                  <small className="text-muted">Perfil</small>
                  <p className="mb-0">Perfil #{user.profileId}</p>
                </div>
                <div className="col-md-3">
                  <small className="text-muted">Nacionalidad</small>
                  <p className="mb-0">Nacionalidad #{user.nationalityId}</p>
                </div>
                <div className="col-md-3">
                  <small className="text-muted">Estado</small>
                  <p className="mb-0">
                    <span className={`badge ${user.isActive ? 'bg-success' : 'bg-danger'}`}>
                      {user.isActive ? 'Activo' : 'Inactivo'}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile 