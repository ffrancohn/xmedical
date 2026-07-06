#!/usr/bin/env python3
"""
Script de inicialización de la base de datos XMedical
"""

import asyncio
from sqlmodel import SQLModel, create_engine, Session
from server.models.user import User
from server.models.user_profile import UserProfile
from server.models.nationality import Nationality
from server.models.document import Document
from server.models.address import Address
from server.models.beneficiary import Beneficiary
from server.models.feedback import Feedback
from server.models.center import Center
from server.services.auth_service import get_password_hash
from server.config import settings

# Crear engine de base de datos
engine = create_engine(settings.DATABASE_URL, echo=True)

def create_tables():
    """Crear todas las tablas"""
    print("Creando tablas...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas exitosamente")

def insert_initial_data():
    """Insertar datos iniciales"""
    print("Insertando datos iniciales...")
    
    with Session(engine) as session:
        # Crear perfiles de usuario
        profiles = [
            UserProfile(id=1, name="Administrador", description="Acceso completo al sistema"),
            UserProfile(id=2, name="Usuario Regular", description="Acceso básico al sistema"),
            UserProfile(id=3, name="Médico", description="Acceso médico especializado")
        ]
        
        for profile in profiles:
            session.add(profile)
        
        # Crear nacionalidades
        nationalities = [
            Nationality(id=1, code="HN", name="Honduras"),
            Nationality(id=2, code="US", name="Estados Unidos"),
            Nationality(id=3, code="MX", name="México"),
            Nationality(id=4, code="GT", name="Guatemala"),
            Nationality(id=5, code="SV", name="El Salvador"),
            Nationality(id=6, code="NI", name="Nicaragua"),
            Nationality(id=7, code="CR", name="Costa Rica"),
            Nationality(id=8, code="PA", name="Panamá")
        ]
        
        for nationality in nationalities:
            session.add(nationality)
        
        # Crear usuario administrador por defecto
        admin_user = User(
            id=1,
            username="admin",
            email="admin@xmedical.com",
            fullName="Administrador del Sistema",
            password=get_password_hash("admin123"),
            profileId=1,
            nationalityId=1,
            isActive=True
        )
        
        session.add(admin_user)
        
        # Crear centros médicos de ejemplo
        medical_centers = [
            Center(
                code="SF001",
                centerType="Hospital",
                name="Hospital General San Felipe",
                address="Tegucigalpa, Honduras",
                phones="+504 2234-5678"
            ),
            Center(
                code="SM002",
                centerType="Clínica",
                name="Clínica Santa María",
                address="San Pedro Sula, Honduras",
                phones="+504 2550-1234"
            )
        ]
        
        for center in medical_centers:
            session.add(center)
        
        session.commit()
        print("✅ Datos iniciales insertados exitosamente")

def main():
    """Función principal"""
    print("🚀 Inicializando base de datos XMedical...")
    
    try:
        # Crear tablas
        create_tables()
        
        # Insertar datos iniciales
        insert_initial_data()
        
        print("\n🎉 Base de datos inicializada correctamente!")
        print("\n📋 Credenciales por defecto:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("\n⚠️  IMPORTANTE: Cambia la contraseña del administrador después del primer login")
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        print("\n🔧 Verifica que:")
        print("   1. PostgreSQL esté instalado y ejecutándose")
        print("   2. La base de datos 'xmedical' exista")
        print("   3. Las credenciales en config.env sean correctas")

if __name__ == "__main__":
    main() 