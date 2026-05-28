#!/usr/bin/env python3
"""
Script simple para iniciar el servidor XMedical
"""

import uvicorn
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Iniciando servidor XMedical...")
    print("📋 Configuración:")
    print("   Host: 0.0.0.0")
    print("   Puerto: 8000")
    print("   Documentación: http://localhost:8000/docs")
    print("   Frontend: http://localhost:3000")
    print()
    print("🔄 Iniciando servidor...")
    print("   Presiona Ctrl+C para detener")
    print()
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        print("\n🔧 Verifica que:")
        print("   1. Todas las dependencias estén instaladas")
        print("   2. La base de datos esté configurada")
        print("   3. El archivo config.env exista") 