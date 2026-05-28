#!/usr/bin/env python3
"""
Script para iniciar el servidor de desarrollo XMedical
"""

import uvicorn
import os
import sys
from pathlib import Path

def check_dependencies():
    """Verificar que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    try:
        import fastapi
        import uvicorn
        import sqlmodel
        import psycopg2
        import pytesseract
        import cv2
        import numpy
        from PIL import Image
        
        print("✅ Todas las dependencias están instaladas")
        return True
        
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("🔧 Ejecuta: pip install -r requirements.txt")
        return False

def check_tesseract():
    """Verificar que Tesseract esté instalado"""
    print("🔍 Verificando Tesseract OCR...")
    
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR está instalado")
        return True
        
    except Exception as e:
        print(f"❌ Tesseract OCR no está configurado: {e}")
        print("🔧 Instala Tesseract OCR desde: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def check_environment():
    """Verificar archivo de configuración"""
    print("🔍 Verificando configuración...")
    
    config_file = Path("config.env")
    if not config_file.exists():
        print("❌ Archivo config.env no encontrado")
        print("🔧 Crea el archivo config.env con la configuración de la base de datos")
        return False
    
    print("✅ Archivo de configuración encontrado")
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando servidor XMedical...")
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar Tesseract
    if not check_tesseract():
        print("⚠️  El servidor iniciará sin funcionalidad OCR")
    
    # Verificar configuración
    if not check_environment():
        sys.exit(1)
    
    print("\n🎯 Configuración del servidor:")
    print("   Host: 0.0.0.0")
    print("   Puerto: 8000")
    print("   Modo: Desarrollo")
    print("   Documentación: http://localhost:8000/docs")
    
    print("\n🚀 Iniciando servidor...")
    print("   Presiona Ctrl+C para detener")
    
    try:
        # Iniciar servidor
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

if __name__ == "__main__":
    main() 