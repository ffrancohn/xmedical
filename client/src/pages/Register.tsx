import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'wouter'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/contexts/AuthContext'
import { Eye, EyeOff, AlertCircle, CheckCircle, Calendar } from 'lucide-react'

// Esquema de validación
const registerSchema = z.object({
  username: z.string()
    .min(3, 'El nombre de usuario debe tener al menos 3 caracteres')
    .max(20, 'El nombre de usuario no puede exceder 20 caracteres')
    .regex(/^[a-zA-Z0-9_]+$/, 'Solo se permiten letras, números y guiones bajos'),
  email: z.string()
    .email('Ingresa un email válido'),
  password: z.string()
    .min(8, 'La contraseña debe tener al menos 8 caracteres')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'La contraseña debe contener al menos una mayúscula, una minúscula y un número'),
  confirmPassword: z.string(),
  fullName: z.string()
    .min(2, 'El nombre completo debe tener al menos 2 caracteres')
    .max(100, 'El nombre completo no puede exceder 100 caracteres'),
  profileId: z.number().min(1, 'Selecciona un perfil'),
  nationalityId: z.number().min(1, 'Selecciona una nacionalidad'),
  phone: z.string().optional(),
  birthDate: z.string().optional(),
  gender: z.string().optional()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Las contraseñas no coinciden",
  path: ["confirmPassword"],
})

type RegisterFormData = z.infer<typeof registerSchema>

const Register: React.FC = () => {
  const { register: registerUser } = useAuth()
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [profiles, setProfiles] = useState([])
  const [nationalities, setNationalities] = useState([])
  const [location, setLocation] = useLocation()

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      profileId: 2, // Usuario regular por defecto
      nationalityId: 1 // Honduras por defecto
    }
  })

  // Cargar datos iniciales
  useEffect(() => {
    // Simular carga de perfiles y nacionalidades
    setProfiles([
      { id: 1, name: 'Administrador' },
      { id: 2, name: 'Usuario Regular' },
      { id: 3, name: 'Médico' }
    ])
    
    setNationalities([
      { id: 1, name: 'Honduras', code: 'HN' },
      { id: 2, name: 'Estados Unidos', code: 'US' },
      { id: 3, name: 'México', code: 'MX' },
      { id: 4, name: 'Guatemala', code: 'GT' },
      { id: 5, name: 'El Salvador', code: 'SV' }
    ])
  }, [])

  const onSubmit = async (data: RegisterFormData) => {
    try {
      setIsLoading(true)
      setError('')
      await registerUser(data)
      setLocation('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Error al registrar usuario')
    } finally {
      setIsLoading(false)
    }
  }

  const password = watch('password')

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center bg-gradient">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6">
            <div className="card shadow-lg border-0">
              <div className="card-body p-5">
                {/* Logo y título */}
                <div className="text-center mb-4">
                  <h2 className="text-gradient fw-bold mb-2">XMedical</h2>
                  <p className="text-muted">Crea tu cuenta</p>
                </div>

                {/* Formulario */}
                <form onSubmit={handleSubmit(onSubmit)}>
                  <div className="row">
                    {/* Nombre completo */}
                    <div className="col-md-6 mb-3">
                      <label htmlFor="fullName" className="form-label">
                        Nombre completo *
                      </label>
                      <input
                        type="text"
                        id="fullName"
                        className={`form-control ${errors.fullName ? 'is-invalid' : ''}`}
                        placeholder="Ingresa tu nombre completo"
                        {...register('fullName')}
                      />
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
                      <input
                        type="email"
                        id="email"
                        className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                        placeholder="Ingresa tu email"
                        {...register('email')}
                      />
                      {errors.email && (
                        <div className="invalid-feedback d-flex align-items-center">
                          <AlertCircle size={16} className="me-1" />
                          {errors.email.message}
                        </div>
                      )}
                    </div>

                    {/* Nombre de usuario */}
                    <div className="col-md-6 mb-3">
                      <label htmlFor="username" className="form-label">
                        Nombre de usuario *
                      </label>
                      <input
                        type="text"
                        id="username"
                        className={`form-control ${errors.username ? 'is-invalid' : ''}`}
                        placeholder="Ingresa tu nombre de usuario"
                        {...register('username')}
                      />
                      {errors.username && (
                        <div className="invalid-feedback d-flex align-items-center">
                          <AlertCircle size={16} className="me-1" />
                          {errors.username.message}
                        </div>
                      )}
                    </div>

                    {/* Teléfono */}
                    <div className="col-md-6 mb-3">
                      <label htmlFor="phone" className="form-label">
                        Teléfono
                      </label>
                      <input
                        type="tel"
                        id="phone"
                        className="form-control"
                        placeholder="Ingresa tu teléfono"
                        {...register('phone')}
                      />
                    </div>

                    {/* Fecha de nacimiento */}
                    <div className="col-md-6 mb-3">
                      <label htmlFor="birthDate" className="form-label">
                        Fecha de nacimiento
                      </label>
                      <div className="position-relative">
                        <input
                          type="date"
                          id="birthDate"
                          className="form-control"
                          {...register('birthDate')}
                        />
                        <Calendar size={16} className="position-absolute top-50 end-0 translate-middle-y me-2 text-muted" />
                      </div>
                    </div>

                    {/* Género */}
                    <div className="col-md-6 mb-3">
                      <label htmlFor="gender" className="form-label">
                        Género
                      </label>
                      <select id="gender" className="form-select" {...register('gender')}>
                        <option value="">Selecciona...</option>
                        <option value="M">Masculino</option>
                        <option value="F">Femenino</option>
                        <option value="O">Otro</option>
                      </select>
                    </div>

                    {/* Perfil */}
                    <div className="col-md-6 mb-3">
                      <label htmlFor="profileId" className="form-label">
                        Perfil *
                      </label>
                      <select 
                        id="profileId" 
                        className={`form-select ${errors.profileId ? 'is-invalid' : ''}`}
                        {...register('profileId', { valueAsNumber: true })}
                      >
                        <option value="">Selecciona un perfil...</option>
                        {profiles.map((profile: any) => (
                          <option key={profile.id} value={profile.id}>
                            {profile.name}
                          </option>
                        ))}
                      </select>
                      {errors.profileId && (
                        <div className="invalid-feedback d-flex align-items-center">
                          <AlertCircle size={16} className="me-1" />
                          {errors.profileId.message}
                        </div>
                      )}
                    </div>

                    {/* Nacionalidad */}
                    <div className="col-md-6 mb-3">
                      <label htmlFor="nationalityId" className="form-label">
                        Nacionalidad *
                      </label>
                      <select 
                        id="nationalityId" 
                        className={`form-select ${errors.nationalityId ? 'is-invalid' : ''}`}
                        {...register('nationalityId', { valueAsNumber: true })}
                      >
                        <option value="">Selecciona una nacionalidad...</option>
                        {nationalities.map((nationality: any) => (
                          <option key={nationality.id} value={nationality.id}>
                            {nationality.name}
                          </option>
                        ))}
                      </select>
                      {errors.nationalityId && (
                        <div className="invalid-feedback d-flex align-items-center">
                          <AlertCircle size={16} className="me-1" />
                          {errors.nationalityId.message}
                        </div>
                      )}
                    </div>

                    {/* Contraseña */}
                    <div className="col-md-6 mb-3">
                      <label htmlFor="password" className="form-label">
                        Contraseña *
                      </label>
                      <div className="position-relative">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          id="password"
                          className={`form-control ${errors.password ? 'is-invalid' : ''}`}
                          placeholder="Ingresa tu contraseña"
                          {...register('password')}
                        />
                        <button
                          type="button"
                          className="btn btn-link position-absolute end-0 top-50 translate-middle-y"
                          onClick={() => setShowPassword(!showPassword)}
                        >
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                      {errors.password && (
                        <div className="invalid-feedback d-flex align-items-center">
                          <AlertCircle size={16} className="me-1" />
                          {errors.password.message}
                        </div>
                      )}
                    </div>

                    {/* Confirmar contraseña */}
                    <div className="col-md-6 mb-4">
                      <label htmlFor="confirmPassword" className="form-label">
                        Confirmar contraseña *
                      </label>
                      <div className="position-relative">
                        <input
                          type={showConfirmPassword ? 'text' : 'password'}
                          id="confirmPassword"
                          className={`form-control ${errors.confirmPassword ? 'is-invalid' : ''}`}
                          placeholder="Confirma tu contraseña"
                          {...register('confirmPassword')}
                        />
                        <button
                          type="button"
                          className="btn btn-link position-absolute end-0 top-50 translate-middle-y"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        >
                          {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                      {errors.confirmPassword && (
                        <div className="invalid-feedback d-flex align-items-center">
                          <AlertCircle size={16} className="me-1" />
                          {errors.confirmPassword.message}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Error general */}
                  {error && (
                    <div className="alert alert-danger d-flex align-items-center mb-3">
                      <AlertCircle size={16} className="me-2" />
                      {error}
                    </div>
                  )}

                  {/* Botón de envío */}
                  <button
                    type="submit"
                    className="btn btn-primary w-100 mb-3"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <div className="loading-spinner me-2"></div>
                        Creando cuenta...
                      </>
                    ) : (
                      'Crear cuenta'
                    )}
                  </button>

                  {/* Enlaces adicionales */}
                  <div className="text-center">
                    <p className="mb-0">
                      ¿Ya tienes una cuenta?{' '}
                      <Link href="/login">
                        <a className="text-decoration-none">Inicia sesión aquí</a>
                      </Link>
                    </p>
                  </div>
                </form>
              </div>
            </div>

            {/* Información adicional */}
            <div className="text-center mt-4">
              <p className="text-white-50 small">
                Sistema de Asistencia Médica Inteligente
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Register 