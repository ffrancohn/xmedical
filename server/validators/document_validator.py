import re
from datetime import datetime, date
from typing import Dict, List, Optional

class DocumentValidator:
    @staticmethod
    def validate_honduran_id(document_number: str) -> Dict[str, any]:
        """
        Valida formato de documento de identidad hondureño (13 dígitos)
        """
        if not document_number:
            return {"valid": False, "error": "Número de documento requerido"}
        
        # Verificar que sean exactamente 13 dígitos
        if not re.match(r'^\d{13}$', document_number):
            return {"valid": False, "error": "El documento debe tener exactamente 13 dígitos"}
        
        # Validar que no sean todos ceros
        if document_number == "0000000000000":
            return {"valid": False, "error": "Número de documento inválido"}
        
        # Validar formato específico de Honduras (primeros 4 dígitos = año de nacimiento)
        try:
            year = int(document_number[:4])
            current_year = datetime.now().year
            
            if year < 1900 or year > current_year:
                return {"valid": False, "error": "Año de nacimiento inválido en el documento"}
            
        except ValueError:
            return {"valid": False, "error": "Formato de documento inválido"}
        
        return {"valid": True, "document_number": document_number}
    
    @staticmethod
    def validate_expiry_date(expiry_date: date) -> Dict[str, any]:
        """
        Valida fecha de vencimiento del documento
        """
        if not expiry_date:
            return {"valid": False, "error": "Fecha de vencimiento requerida"}
        
        today = date.today()
        
        if expiry_date < today:
            return {"valid": False, "error": "El documento ha expirado"}
        
        # Verificar que no sea más de 10 años en el futuro
        max_future_date = date(today.year + 10, today.month, today.day)
        if expiry_date > max_future_date:
            return {"valid": False, "error": "Fecha de vencimiento muy lejana"}
        
        return {"valid": True, "expiry_date": expiry_date}
    
    @staticmethod
    def validate_document_type(document_type: str) -> Dict[str, any]:
        """
        Valida tipo de documento permitido
        """
        allowed_types = [
            "DNI", "Identidad", "Cédula", "Pasaporte", "Licencia", 
            "Carnet de Extranjero", "Tarjeta de Residencia"
        ]
        
        if not document_type:
            return {"valid": False, "error": "Tipo de documento requerido"}
        
        if document_type not in allowed_types:
            return {"valid": False, "error": f"Tipo de documento no permitido. Tipos válidos: {', '.join(allowed_types)}"}
        
        return {"valid": True, "document_type": document_type} 