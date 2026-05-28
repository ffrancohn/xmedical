from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.user_profiles import router as profiles_router
from routes.nationalities import router as nationalities_router
from routes.addresses import router as addresses_router
from routes.documents import router as documents_router
from routes.beneficiaries import router as beneficiaries_router
from routes.feedback import router as feedback_router
from routes.centers import router as centers_router
from routes.biometric import router as biometric_router
from routes.upload import router as upload_router
import os

app = FastAPI(
    title="XMedical API",
    description="API para el sistema de asistencia médica inteligente XMedical",
    version="1.0.0",
    contact={
        "name": "XMedical Development Team",
        "email": "support@xmedical.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(profiles_router)
app.include_router(nationalities_router)
app.include_router(addresses_router)
app.include_router(documents_router)
app.include_router(beneficiaries_router)
app.include_router(feedback_router)
app.include_router(centers_router)
app.include_router(biometric_router)
app.include_router(upload_router)

# Servir archivos estáticos de uploads
uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/")
def read_root():
    return {
        "mensaje": "¡XMedical Backend en funcionamiento!",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"} 