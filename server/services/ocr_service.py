import pytesseract
from PIL import Image
import io
import base64
import re
from typing import Dict, Optional

class OCRService:
    @staticmethod
    def extract_text_from_image(image_data: str) -> Dict[str, any]:
        """
        Extrae texto de una imagen usando OCR
        """
        try:
            # Decodificar imagen base64
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Extraer texto usando Tesseract
            text = pytesseract.image_to_string(image, lang='spa+eng')
            
            # Procesar y extraer información específica
            extracted_data = OCRService._parse_document_text(text)
            
            return {
                "success": True,
                "raw_text": text,
                "extracted_data": extracted_data,
                "confidence_score": OCRService._calculate_confidence(text)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "raw_text": "",
                "extracted_data": {},
                "confidence_score": 0.0
            }
    
    @staticmethod
    def _parse_document_text(text: str) -> Dict[str, any]:
        """
        Parsea el texto extraído para obtener información específica del documento
        """
        data = {}
        
        # Buscar número de documento (13 dígitos para Honduras)
        doc_pattern = r'\b\d{13}\b'
        doc_match = re.search(doc_pattern, text)
        if doc_match:
            data['document_number'] = doc_match.group()
        
        # Buscar fechas
        date_patterns = [
            r'\b\d{2}/\d{2}/\d{4}\b',
            r'\b\d{2}-\d{2}-\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        if dates:
            data['dates'] = dates
        
        # Buscar nombres (patrón básico)
        name_pattern = r'[A-Z][a-z]+ [A-Z][a-z]+'
        names = re.findall(name_pattern, text)
        if names:
            data['names'] = names
        
        return data
    
    @staticmethod
    def _calculate_confidence(text: str) -> float:
        """
        Calcula un score de confianza basado en la calidad del texto extraído
        """
        if not text.strip():
            return 0.0
        
        # Métricas básicas de confianza
        lines = text.strip().split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Porcentaje de líneas no vacías
        line_confidence = len(non_empty_lines) / max(len(lines), 1)
        
        # Longitud promedio de líneas
        avg_line_length = sum(len(line) for line in non_empty_lines) / max(len(non_empty_lines), 1)
        length_confidence = min(avg_line_length / 50, 1.0)  # Normalizar a 50 caracteres
        
        # Score final
        confidence = (line_confidence + length_confidence) / 2
        return round(confidence, 2) 