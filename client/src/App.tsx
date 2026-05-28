import { Route, Switch } from 'wouter'
import { AuthProvider } from '@/contexts/AuthContext'
import { ThemeProvider } from '@/contexts/ThemeContext'
import Layout from '@/components/Layout/Layout'
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import Dashboard from '@/pages/Dashboard'
import Profile from '@/pages/Profile'
import Documents from '@/pages/Documents'
import Addresses from '@/pages/Addresses'
import Beneficiaries from '@/pages/Beneficiaries'
import Feedback from '@/pages/Feedback'
import Admin from '@/pages/Admin'
import ProtectedRoute from '@/components/Auth/ProtectedRoute'

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Switch>
          {/* Rutas públicas */}
          <Route path="/" component={Login} />
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          
          {/* Rutas protegidas */}
          <Route path="/dashboard">
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          </Route>
          
          <Route path="/profile">
            <ProtectedRoute>
              <Layout>
                <Profile />
              </Layout>
            </ProtectedRoute>
          </Route>
          
          <Route path="/documents">
            <ProtectedRoute>
              <Layout>
                <Documents />
              </Layout>
            </ProtectedRoute>
          </Route>
          
          <Route path="/addresses">
            <ProtectedRoute>
              <Layout>
                <Addresses />
              </Layout>
            </ProtectedRoute>
          </Route>
          
          <Route path="/beneficiaries">
            <ProtectedRoute>
              <Layout>
                <Beneficiaries />
              </Layout>
            </ProtectedRoute>
          </Route>
          
          <Route path="/feedback">
            <ProtectedRoute>
              <Layout>
                <Feedback />
              </Layout>
            </ProtectedRoute>
          </Route>
          
          <Route path="/admin">
            <ProtectedRoute requireAdmin>
              <Layout>
                <Admin />
              </Layout>
            </ProtectedRoute>
          </Route>
          
          {/* Ruta 404 */}
          <Route>
            <div className="container mt-5">
              <div className="row justify-content-center">
                <div className="col-md-6 text-center">
                  <h1 className="display-1">404</h1>
                  <h2>Página no encontrada</h2>
                  <p className="lead">La página que buscas no existe.</p>
                  <a href="/" className="btn btn-primary">Volver al inicio</a>
                </div>
              </div>
            </div>
          </Route>
        </Switch>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App 