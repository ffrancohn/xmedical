#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos PostgreSQL
"""

import psycopg2
from psycopg2 import OperationalError
from config import settings

def test_connection():
    """Probar conexión a PostgreSQL"""
    print("🔍 Probando conexión a PostgreSQL...")
    
    try:
        # Extraer información de la URL de conexión
        db_url = settings.DATABASE_URL
        print(f"URL de conexión: {db_url}")
        
        # Intentar conectar
        conn = psycopg2.connect(db_url)
        
        # Crear cursor
        cur = conn.cursor()
        
        # Ejecutar consulta simple
        cur.execute("SELECT version();")
        
        # Obtener resultado
        version = cur.fetchone()
        print(f"✅ Conexión exitosa!")
        print(f"📋 Versión de PostgreSQL: {version[0]}")
        
        # Verificar si la base de datos existe
        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()[0]
        print(f"📊 Base de datos actual: {db_name}")
        
        # Cerrar conexión
        cur.close()
        conn.close()
        
        return True
        
    except OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Posibles soluciones:")
        print("   1. Verifica que PostgreSQL esté instalado y ejecutándose")
        print("   2. Verifica que la base de datos 'xmedical' exista")
        print("   3. Verifica las credenciales en config.env")
        print("   4. Asegúrate de que el puerto 5432 esté disponible")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def create_database():
    """Crear la base de datos si no existe"""
    print("\n🗄️  Creando base de datos 'xmedical'...")
    
    try:
        # Conectar a PostgreSQL sin especificar base de datos
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="password"  # Cambia esto por tu contraseña
        )
        
        conn.autocommit = True
        cur = conn.cursor()
        
        # Verificar si la base de datos existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname='xmedical'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute("CREATE DATABASE xmedical")
            print("✅ Base de datos 'xmedical' creada exitosamente")
        else:
            print("ℹ️  La base de datos 'xmedical' ya existe")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear la base de datos: {e}")
        print("\n🔧 Instrucciones manuales:")
        print("   1. Abre pgAdmin o psql")
        print("   2. Conecta como usuario postgres")
        print("   3. Ejecuta: CREATE DATABASE xmedical;")
        return False

def main():
    """Función principal"""
    print("🚀 Verificando configuración de PostgreSQL...")
    
    # Primero intentar crear la base de datos
    if create_database():
        # Luego probar la conexión
        if test_connection():
            print("\n🎉 PostgreSQL está configurado correctamente!")
            print("✅ Puedes continuar con la inicialización de la base de datos")
        else:
            print("\n❌ No se pudo conectar a PostgreSQL")
    else:
        print("\n❌ No se pudo crear la base de datos")

if __name__ == "__main__":
    main() 