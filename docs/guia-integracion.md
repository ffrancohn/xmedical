# Guía de Integración - XMedical Backend (FastAPI — LEGADO)

> **Documento histórico.** Describe la integración del frontend React (`client/`) con el backend FastAPI (`server/`).
>
> El stack activo usa **Django con plantillas server-side** y no requiere esta guía. Ver [`README.md`](../README.md).

## Descripción General

Esta guía proporcionaba la información necesaria para integrar el frontend React de XMedical con el backend FastAPI del prototipo inicial.

## Configuración Base

### URL Base
```
http://localhost:8000
```

### Headers Requeridos
Para endpoints protegidos, incluir el token JWT:
```javascript
headers: {
  'Authorization': 'Bearer <access_token>',
  'Content-Type': 'application/json'
}
```

## Autenticación

### 1. Registro de Usuario
```javascript
const registerUser = async (userData) => {
  const response = await fetch('http://localhost:8000/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: userData.username,
      email: userData.email,
      password: userData.password,
      fullName: userData.fullName,
      profileId: userData.profileId,
      nationalityId: userData.nationalityId,
      phone: userData.phone,
      birthDate: userData.birthDate,
      gender: userData.gender
    })
  });
  
  return await response.json();
};
```

### 2. Login
```javascript
const loginUser = async (credentials) => {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: credentials.username,
      password: credentials.password
    })
  });
  
  const data = await response.json();
  
  // Guardar tokens
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  
  return data;
};
```

### 3. Refresh Token
```javascript
const refreshToken = async () => {
  const refresh_token = localStorage.getItem('refresh_token');
  
  const response = await fetch('http://localhost:8000/auth/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      refresh_token: refresh_token
    })
  });
  
  const data = await response.json();
  
  // Actualizar tokens
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  
  return data;
};
```

## Gestión de Usuarios

### Obtener Perfil del Usuario Actual
```javascript
const getCurrentUser = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/users/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
};
```

### Listar Usuarios (Solo Administradores)
```javascript
const listUsers = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/users/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
};
```

## Gestión de Documentos

### Subir Documento
```javascript
const uploadDocument = async (file) => {
  const token = localStorage.getItem('access_token');
  
  // Primero subir el archivo
  const formData = new FormData();
  formData.append('file', file);
  
  const uploadResponse = await fetch('http://localhost:8000/upload/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  const uploadData = await uploadResponse.json();
  
  // Luego crear el documento
  const documentResponse = await fetch('http://localhost:8000/documents/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userId: currentUser.id,
      documentType: 'DNI',
      documentNumber: '1234567890123',
      frontImageUrl: uploadData.url,
      backImageUrl: null,
      isValid: false
    })
  });
  
  return await documentResponse.json();
};
```

### Listar Documentos
```javascript
const listDocuments = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/documents/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
};
```

## Verificación Biométrica

### Procesar OCR de Documento
```javascript
const processDocumentOCR = async (imageData) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/biometric/ocr/process', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      image_data: imageData // Base64 string
    })
  });
  
  return await response.json();
};
```

### Verificación Facial
```javascript
const verifyFacialIdentity = async (documentPhoto, livePhoto) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/biometric/facial/verify', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      document_photo: documentPhoto, // Base64 string
      live_photo: livePhoto // Base64 string
    })
  });
  
  return await response.json();
};
```

## Gestión de Direcciones

### Crear Dirección
```javascript
const createAddress = async (addressData) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/addresses/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userId: currentUser.id,
      country: addressData.country,
      state: addressData.state,
      city: addressData.city,
      zipCode: addressData.zipCode,
      fullAddress: addressData.fullAddress,
      exteriorNumber: addressData.exteriorNumber,
      interiorNumber: addressData.interiorNumber,
      latitude: addressData.latitude,
      longitude: addressData.longitude
    })
  });
  
  return await response.json();
};
```

## Gestión de Beneficiarios

### Crear Beneficiario
```javascript
const createBeneficiary = async (beneficiaryData) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/beneficiaries/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userId: currentUser.id,
      fullName: beneficiaryData.fullName,
      documentNumber: beneficiaryData.documentNumber,
      relationship: beneficiaryData.relationship,
      birthDate: beneficiaryData.birthDate
    })
  });
  
  return await response.json();
};
```

## Sistema de Feedback

### Crear Feedback
```javascript
const createFeedback = async (feedbackData) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/feedback/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userId: currentUser.id,
      type: feedbackData.type, // 'Sugerencia', 'Queja', 'Elogio', 'Bug', 'Feature Request', 'General'
      subject: feedbackData.subject,
      message: feedbackData.message,
      priority: feedbackData.priority, // 'Baja', 'Media', 'Alta', 'Crítica'
      status: 'Pendiente'
    })
  });
  
  return await response.json();
};
```

## Manejo de Errores

### Interceptor para Tokens Expirados
```javascript
const apiCall = async (url, options = {}) => {
  const token = localStorage.getItem('access_token');
  
  const config = {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers
    }
  };
  
  try {
    const response = await fetch(url, config);
    
    if (response.status === 401) {
      // Token expirado, intentar refresh
      const refreshResult = await refreshToken();
      if (refreshResult.access_token) {
        // Reintentar la llamada original
        config.headers.Authorization = `Bearer ${refreshResult.access_token}`;
        return await fetch(url, config);
      } else {
        // Redirigir al login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }
    
    return response;
  } catch (error) {
    console.error('Error en llamada API:', error);
    throw error;
  }
};
```

## Validaciones Frontend

### Validación de Contraseña
```javascript
const validatePassword = (password) => {
  const errors = [];
  
  if (password.length < 8) {
    errors.push('La contraseña debe tener al menos 8 caracteres');
  }
  
  if (!/[A-Z]/.test(password)) {
    errors.push('Debe contener al menos una letra mayúscula');
  }
  
  if (!/[a-z]/.test(password)) {
    errors.push('Debe contener al menos una letra minúscula');
  }
  
  if (!/\d/.test(password)) {
    errors.push('Debe contener al menos un número');
  }
  
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('Debe contener al menos un carácter especial');
  }
  
  return errors;
};
```

### Validación de Documento Hondureño
```javascript
const validateHonduranDocument = (documentNumber) => {
  if (!/^\d{13}$/.test(documentNumber)) {
    return 'El documento debe tener exactamente 13 dígitos';
  }
  
  if (documentNumber === '0000000000000') {
    return 'Número de documento inválido';
  }
  
  const year = parseInt(documentNumber.substring(0, 4));
  const currentYear = new Date().getFullYear();
  
  if (year < 1900 || year > currentYear) {
    return 'Año de nacimiento inválido en el documento';
  }
  
  return null; // Válido
};
```

## Configuración de Entorno

### Variables de Entorno Frontend
```javascript
// .env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_UPLOAD_URL=http://localhost:8000/upload
REACT_APP_DOCS_URL=http://localhost:8000/docs
```

### Configuración de TanStack Query
```javascript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      {/* Tu aplicación */}
    </QueryClientProvider>
  );
}
```

## Ejemplos de Uso Completo

### Flujo de Registro Completo
```javascript
const completeRegistration = async (userData) => {
  try {
    // 1. Registrar usuario
    const user = await registerUser(userData);
    
    // 2. Login automático
    const loginResult = await loginUser({
      username: userData.username,
      password: userData.password
    });
    
    // 3. Subir documento
    const documentResult = await uploadDocument(userData.documentFile);
    
    // 4. Procesar OCR
    const ocrResult = await processDocumentOCR(userData.documentImage);
    
    // 5. Verificación facial
    const facialResult = await verifyFacialIdentity(
      userData.documentPhoto,
      userData.livePhoto
    );
    
    // 6. Crear dirección
    const addressResult = await createAddress(userData.address);
    
    return {
      success: true,
      user: user,
      document: documentResult,
      ocr: ocrResult,
      facial: facialResult,
      address: addressResult
    };
    
  } catch (error) {
    console.error('Error en registro:', error);
    throw error;
  }
};
```

## Notas Importantes

1. **CORS**: El backend está configurado para permitir todas las origenes en desarrollo. En producción, especificar dominios específicos.

2. **Tokens**: Los tokens JWT tienen una duración de 30 minutos (access) y 7 días (refresh).

3. **Archivos**: Los archivos subidos se guardan en `/uploads/` y son accesibles públicamente.

4. **Validaciones**: Implementar validaciones tanto en frontend como backend para mejor UX.

5. **Errores**: Manejar errores HTTP apropiadamente y mostrar mensajes útiles al usuario.

## Recursos Adicionales

- **Documentación API**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health 