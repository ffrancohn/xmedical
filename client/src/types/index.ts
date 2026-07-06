// Tipos de usuario
export interface User {
  id: number
  username: string
  email: string
  fullName: string
  profileId: number
  nationalityId: number
  phone?: string
  birthDate?: string
  gender?: string
  isActive: boolean
  themeMode?: string
  colorTheme?: string
}

export interface UserProfile {
  id: number
  name: string
  description?: string
  permissions?: string
}

export interface Nationality {
  id: number
  code: string
  name: string
}

// Tipos de autenticación
export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  fullName: string
  profileId: number
  nationalityId: number
  phone?: string
  birthDate?: string
  gender?: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
}

// Tipos de documentos
export interface Document {
  id: number
  userId: number
  documentType: string
  documentNumber: string
  expiryDate?: string
  frontImageUrl?: string
  backImageUrl?: string
  ocrData?: string
  isValid: boolean
}

export interface DocumentCreate {
  userId: number
  documentType: string
  documentNumber: string
  expiryDate?: string
  frontImageUrl?: string
  backImageUrl?: string
  ocrData?: string
  isValid?: boolean
}

// Tipos de direcciones
export interface Address {
  id: number
  userId: number
  country: string
  state: string
  city: string
  zipCode?: string
  fullAddress: string
  exteriorNumber?: string
  interiorNumber?: string
  latitude?: number
  longitude?: number
}

export interface AddressCreate {
  userId: number
  country: string
  state: string
  city: string
  zipCode?: string
  fullAddress: string
  exteriorNumber?: string
  interiorNumber?: string
  latitude?: number
  longitude?: number
}

// Tipos de beneficiarios
export interface Beneficiary {
  id: number
  userId: number
  fullName: string
  documentNumber: string
  relationship: string
  birthDate?: string
}

export interface BeneficiaryCreate {
  userId: number
  fullName: string
  documentNumber: string
  relationship: string
  birthDate?: string
}

// Tipos de feedback
export interface Feedback {
  id: number
  userId: number
  type: string
  subject: string
  message: string
  priority: string
  status: string
  response?: string
  respondedBy?: number
}

export interface FeedbackCreate {
  userId: number
  type: string
  subject: string
  message: string
  priority: string
  status: string
  response?: string
  respondedBy?: number
}

// Tipos de centros médicos
export interface Center {
  id: number
  code: string
  centerType: string
  name: string
  address: string
  phones?: string
}

export interface CenterCreate {
  code: string
  centerType: string
  name: string
  address: string
  phones?: string
}

// Tipos de verificación biométrica
export interface FacialVerification {
  id: number
  userId: number
  documentPhotoUrl?: string
  livePhotoUrl?: string
  verificationScore?: number
  isValid: boolean
}

export interface FacialVerificationCreate {
  userId: number
  documentPhotoUrl?: string
  livePhotoUrl?: string
  verificationScore?: number
  isValid?: boolean
}

// Tipos de OCR
export interface OCRResult {
  success: boolean
  extracted_data?: {
    document_number?: string
    dates?: string[]
    names?: string[]
  }
  confidence_score?: number
  raw_text?: string
  error?: string
}

// Tipos de verificación facial
export interface FacialVerificationResult {
  success: boolean
  verification_score?: number
  is_match?: boolean
  distance?: number
  error?: string
  quality_analysis?: {
    document_photo: ImageQualityResult
    live_photo: ImageQualityResult
  }
}

export interface ImageQualityResult {
  success: boolean
  quality_score: number
  face_count: number
  issues: string[]
  is_suitable: boolean
  error?: string
}

// Tipos de subida de archivos
export interface UploadResult {
  success: boolean
  url: string
  filename: string
}

// Tipos de respuesta de API
export interface ApiResponse<T> {
  data?: T
  message?: string
  success: boolean
  error?: string
}

// Tipos de tema
export interface Theme {
  mode: 'light' | 'dark'
  color: 'blue' | 'green' | 'purple' | 'orange' | 'red' | 'slate'
}

// Tipos de navegación
export interface MenuItem {
  id: string
  label: string
  icon: string
  path: string
  children?: MenuItem[]
  requiresAdmin?: boolean
}

// Tipos de formularios
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'select' | 'textarea' | 'date' | 'file'
  required?: boolean
  options?: { value: string; label: string }[]
  validation?: any
}

// Tipos de notificaciones
export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

// Tipos de paginación
export interface Pagination {
  page: number
  limit: number
  total: number
  totalPages: number
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: Pagination
} 