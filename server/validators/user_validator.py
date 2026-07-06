import re
from datetime import date, datetime
from typing import Dict, Optional

class UserValidator:
    @staticmethod
    def validate_password(password: str) -> Dict[str, any]:
        """
        Valida contraseña según políticas de seguridad
        """
        if not password:
            return {"valid": False, "error": "Contraseña requerida"}
        
        if len(password) < 8:
            return {"valid": False, "error": "La contraseña debe tener al menos 8 caracteres"}
        
        if len(password) > 128:
            return {"valid": False, "error": "La contraseña no puede exceder 128 caracteres"}
        
        # Verificar que contenga al menos una letra mayúscula
        if not re.search(r'[A-Z]', password):
            return {"valid": False, "error": "La contraseña debe contener al menos una letra mayúscula"}
        
        # Verificar que contenga al menos una letra minúscula
        if not re.search(r'[a-z]', password):
            return {"valid": False, "error": "La contraseña debe contener al menos una letra minúscula"}
        
        # Verificar que contenga al menos un número
        if not re.search(r'\d', password):
            return {"valid": False, "error": "La contraseña debe contener al menos un número"}
        
        # Verificar que contenga al menos un carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return {"valid": False, "error": "La contraseña debe contener al menos un carácter especial"}
        
        return {"valid": True, "password": password}
    
    @staticmethod
    def validate_email(email: str) -> Dict[str, any]:
        """
        Valida formato de email
        """
        if not email:
            return {"valid": False, "error": "Email requerido"}
        
        # Patrón básico de validación de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return {"valid": False, "error": "Formato de email inválido"}
        
        # Verificar longitud
        if len(email) > 254:
            return {"valid": False, "error": "Email demasiado largo"}
        
        return {"valid": True, "email": email}
    
    @staticmethod
    def validate_phone(phone: str) -> Dict[str, any]:
        """
        Valida formato de teléfono hondureño
        """
        if not phone:
            return {"valid": True, "phone": None}  # Teléfono es opcional
        
        # Remover espacios y caracteres especiales
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
        
        # Verificar que sean solo números
        if not clean_phone.isdigit():
            return {"valid": False, "error": "El teléfono debe contener solo números"}
        
        # Verificar longitud (8 dígitos para Honduras)
        if len(clean_phone) != 8:
            return {"valid": False, "error": "El teléfono debe tener 8 dígitos"}
        
        return {"valid": True, "phone": clean_phone}
    
    @staticmethod
    def validate_birth_date(birth_date: date) -> Dict[str, any]:
        """
        Valida fecha de nacimiento
        """
        if not birth_date:
            return {"valid": True, "birth_date": None}  # Fecha de nacimiento es opcional
        
        today = date.today()
        
        # Verificar que no sea en el futuro
        if birth_date > today:
            return {"valid": False, "error": "La fecha de nacimiento no puede ser en el futuro"}
        
        # Verificar edad mínima (18 años)
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return {"valid": False, "error": "El usuario debe ser mayor de 18 años"}
        
        # Verificar edad máxima (120 años)
        if age > 120:
            return {"valid": False, "error": "Fecha de nacimiento inválida"}
        
        return {"valid": True, "birth_date": birth_date, "age": age}
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, any]:
        """
        Valida formato de nombre de usuario
        """
        if not username:
            return {"valid": False, "error": "Nombre de usuario requerido"}
        
        # Verificar longitud
        if len(username) < 3:
            return {"valid": False, "error": "El nombre de usuario debe tener al menos 3 caracteres"}
        
        if len(username) > 50:
            return {"valid": False, "error": "El nombre de usuario no puede exceder 50 caracteres"}
        
        # Verificar que solo contenga letras, números y guiones bajos
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return {"valid": False, "error": "El nombre de usuario solo puede contener letras, números y guiones bajos"}
        
        # Verificar que no empiece con número
        if username[0].isdigit():
            return {"valid": False, "error": "El nombre de usuario no puede empezar con un número"}
        
        return {"valid": True, "username": username} 