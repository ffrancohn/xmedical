import React, { ReactNode } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { Navigate } from 'wouter'

interface ProtectedRouteProps {
  children: ReactNode
  requireAdmin?: boolean
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requireAdmin = false 
}) => {
  const { isAuthenticated, isLoading, user } = useAuth()

  // Mostrar loading mientras se verifica la autenticación
  if (isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <div className="text-center">
          <div className="loading-spinner mb-3"></div>
          <p className="text-muted">Verificando autenticación...</p>
        </div>
      </div>
    )
  }

  // Si no está autenticado, redirigir al login
  if (!isAuthenticated) {
    return <Navigate to="/login" />
  }

  // Si requiere admin y el usuario no es admin, redirigir al dashboard
  if (requireAdmin && user?.profileId !== 1) {
    return <Navigate to="/dashboard" />
  }

  return <>{children}</>
}

export default ProtectedRoute 