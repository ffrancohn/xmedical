import { AuthTokens, LoginCredentials, RegisterData, User } from '@/types'

// Configuración de la API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Clase para manejar errores de API
class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

// Función para obtener headers con autenticación
const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem('access_token')
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  }
}

// Función para manejar respuestas de la API
const handleResponse = async (response: Response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new ApiError(
      errorData.detail || `HTTP error! status: ${response.status}`,
      response.status,
      errorData
    )
  }
  return response.json()
}

// Función para refresh token
const refreshToken = async (): Promise<AuthTokens> => {
  const refresh_token = localStorage.getItem('refresh_token')
  if (!refresh_token) {
    throw new ApiError('No refresh token available', 401)
  }

  const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token }),
  })

  const data = await handleResponse(response)
  
  // Actualizar tokens en localStorage
  localStorage.setItem('access_token', data.access_token)
  localStorage.setItem('refresh_token', data.refresh_token)
  
  return data
}

// Función para hacer llamadas a la API con manejo automático de refresh
const apiCall = async <T>(
  url: string,
  options: RequestInit = {}
): Promise<T> => {
  const config: RequestInit = {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...options.headers,
    },
  }

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, config)
    
    if (response.status === 401) {
      // Token expirado, intentar refresh
      try {
        await refreshToken()
        // Reintentar la llamada original con el nuevo token
        config.headers = getAuthHeaders()
        const retryResponse = await fetch(`${API_BASE_URL}${url}`, config)
        return handleResponse(retryResponse)
      } catch (refreshError) {
        // Refresh falló, limpiar tokens y redirigir al login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        throw refreshError
      }
    }
    
    return handleResponse(response)
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError('Network error', 0, error)
  }
}

// Servicios de autenticación
export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthTokens> => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    })

    const data = await handleResponse(response)
    
    // Guardar tokens
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    
    return data
  },

  register: async (userData: RegisterData): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    })

    return handleResponse(response)
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    window.location.href = '/login'
  },

  getCurrentUser: async (): Promise<User> => {
    return apiCall<User>('/users/me')
  },
}

// Servicios de usuarios
export const userService = {
  getUsers: async (): Promise<User[]> => {
    return apiCall<User[]>('/users/')
  },

  getUser: async (id: number): Promise<User> => {
    return apiCall<User>(`/users/${id}`)
  },

  updateUser: async (id: number, userData: Partial<User>): Promise<User> => {
    return apiCall<User>(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    })
  },

  deleteUser: async (id: number): Promise<void> => {
    return apiCall<void>(`/users/${id}`, {
      method: 'DELETE',
    })
  },
}

// Servicios de documentos
export const documentService = {
  getDocuments: async (): Promise<Document[]> => {
    return apiCall<Document[]>('/documents/')
  },

  getDocument: async (id: number): Promise<Document> => {
    return apiCall<Document>(`/documents/${id}`)
  },

  createDocument: async (documentData: DocumentCreate): Promise<Document> => {
    return apiCall<Document>('/documents/', {
      method: 'POST',
      body: JSON.stringify(documentData),
    })
  },

  updateDocument: async (id: number, documentData: DocumentCreate): Promise<Document> => {
    return apiCall<Document>(`/documents/${id}`, {
      method: 'PUT',
      body: JSON.stringify(documentData),
    })
  },

  deleteDocument: async (id: number): Promise<void> => {
    return apiCall<void>(`/documents/${id}`, {
      method: 'DELETE',
    })
  },
}

// Servicios de direcciones
export const addressService = {
  getAddresses: async (): Promise<Address[]> => {
    return apiCall<Address[]>('/addresses/')
  },

  getAddress: async (id: number): Promise<Address> => {
    return apiCall<Address>(`/addresses/${id}`)
  },

  createAddress: async (addressData: AddressCreate): Promise<Address> => {
    return apiCall<Address>('/addresses/', {
      method: 'POST',
      body: JSON.stringify(addressData),
    })
  },

  updateAddress: async (id: number, addressData: AddressCreate): Promise<Address> => {
    return apiCall<Address>(`/addresses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(addressData),
    })
  },

  deleteAddress: async (id: number): Promise<void> => {
    return apiCall<void>(`/addresses/${id}`, {
      method: 'DELETE',
    })
  },
}

// Servicios de beneficiarios
export const beneficiaryService = {
  getBeneficiaries: async (): Promise<Beneficiary[]> => {
    return apiCall<Beneficiary[]>('/beneficiaries/')
  },

  getBeneficiary: async (id: number): Promise<Beneficiary> => {
    return apiCall<Beneficiary>(`/beneficiaries/${id}`)
  },

  createBeneficiary: async (beneficiaryData: BeneficiaryCreate): Promise<Beneficiary> => {
    return apiCall<Beneficiary>('/beneficiaries/', {
      method: 'POST',
      body: JSON.stringify(beneficiaryData),
    })
  },

  updateBeneficiary: async (id: number, beneficiaryData: BeneficiaryCreate): Promise<Beneficiary> => {
    return apiCall<Beneficiary>(`/beneficiaries/${id}`, {
      method: 'PUT',
      body: JSON.stringify(beneficiaryData),
    })
  },

  deleteBeneficiary: async (id: number): Promise<void> => {
    return apiCall<void>(`/beneficiaries/${id}`, {
      method: 'DELETE',
    })
  },
}

// Servicios de feedback
export const feedbackService = {
  getFeedback: async (): Promise<Feedback[]> => {
    return apiCall<Feedback[]>('/feedback/')
  },

  getFeedbackItem: async (id: number): Promise<Feedback> => {
    return apiCall<Feedback>(`/feedback/${id}`)
  },

  createFeedback: async (feedbackData: FeedbackCreate): Promise<Feedback> => {
    return apiCall<Feedback>('/feedback/', {
      method: 'POST',
      body: JSON.stringify(feedbackData),
    })
  },

  updateFeedback: async (id: number, feedbackData: FeedbackCreate): Promise<Feedback> => {
    return apiCall<Feedback>(`/feedback/${id}`, {
      method: 'PUT',
      body: JSON.stringify(feedbackData),
    })
  },

  deleteFeedback: async (id: number): Promise<void> => {
    return apiCall<void>(`/feedback/${id}`, {
      method: 'DELETE',
    })
  },
}

// Servicios de verificación biométrica
export const biometricService = {
  processOCR: async (imageData: string): Promise<OCRResult> => {
    return apiCall<OCRResult>('/biometric/ocr/process', {
      method: 'POST',
      body: JSON.stringify({ image_data: imageData }),
    })
  },

  verifyFacial: async (documentPhoto: string, livePhoto: string): Promise<FacialVerificationResult> => {
    return apiCall<FacialVerificationResult>('/biometric/facial/verify', {
      method: 'POST',
      body: JSON.stringify({
        document_photo: documentPhoto,
        live_photo: livePhoto,
      }),
    })
  },

  getVerifications: async (): Promise<FacialVerification[]> => {
    return apiCall<FacialVerification[]>('/biometric/verifications')
  },

  getVerification: async (id: number): Promise<FacialVerification> => {
    return apiCall<FacialVerification>(`/biometric/verifications/${id}`)
  },
}

// Servicios de subida de archivos
export const uploadService = {
  uploadFile: async (file: File): Promise<UploadResult> => {
    const formData = new FormData()
    formData.append('file', file)

    const token = localStorage.getItem('access_token')
    const response = await fetch(`${API_BASE_URL}/upload/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    })

    return handleResponse(response)
  },
}

// Exportar tipos necesarios
export type { Document, DocumentCreate, Address, AddressCreate, Beneficiary, BeneficiaryCreate, Feedback, FeedbackCreate, FacialVerification, OCRResult, FacialVerificationResult, UploadResult } 