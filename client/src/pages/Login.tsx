import React, { useState } from 'react'
import { Link, useLocation } from 'wouter'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/contexts/AuthContext'
import { Eye, EyeOff, AlertCircle, CheckCircle } from 'lucide-react'

// Esquema de validación
const loginSchema = z.object({
  username: z.string().min(1, 'El nombre de usuario es requerido'),
  password: z.string().min(1, 'La contraseña es requerida')
})

type LoginFormData = z.infer<typeof loginSchema>

const Login: React.FC = () => {
  const { login } = useAuth()
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [location, setLocation] = useLocation()

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema)
  })

  const onSubmit = async (data: LoginFormData) => {
    try {
      setIsLoading(true)
      setError('')
      await login(data)
      setLocation('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Error al iniciar sesión')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center bg-gradient">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-4">
            <div className="card shadow-lg border-0">
              <div className="card-body p-5">
                {/* Logo y título */}
                <div className="text-center mb-4">
                  <h2 className="text-gradient fw-bold mb-2">XMedical</h2>
                  <p className="text-muted">Inicia sesión en tu cuenta</p>
                </div>

                {/* Formulario */}
                <form onSubmit={handleSubmit(onSubmit)}>
                  {/* Nombre de usuario */}
                  <div className="mb-3">
                    <label htmlFor="username" className="form-label">
                      Nombre de usuario
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

                  {/* Contraseña */}
                  <div className="mb-4">
                    <label htmlFor="password" className="form-label">
                      Contraseña
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
                        Iniciando sesión...
                      </>
                    ) : (
                      'Iniciar sesión'
                    )}
                  </button>

                  {/* Enlaces adicionales */}
                  <div className="text-center">
                    <p className="mb-2">
                      ¿No tienes una cuenta?{' '}
                      <Link href="/register">
                        <a className="text-decoration-none">Regístrate aquí</a>
                      </Link>
                    </p>
                    <a href="#" className="text-decoration-none small">
                      ¿Olvidaste tu contraseña?
                    </a>
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

export default Login 