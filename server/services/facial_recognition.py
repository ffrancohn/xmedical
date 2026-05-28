import face_recognition
import numpy as np
from PIL import Image
import io
import base64
from typing import Dict, Optional

class FacialRecognitionService:
    @staticmethod
    def compare_faces(document_photo: str, live_photo: str) -> Dict[str, any]:
        """
        Compara dos fotos para verificar si es la misma persona
        """
        try:
            # Decodificar imágenes
            doc_encoding = FacialRecognitionService._get_face_encoding(document_photo)
            live_encoding = FacialRecognitionService._get_face_encoding(live_photo)
            
            if doc_encoding is None or live_encoding is None:
                return {
                    "success": False,
                    "error": "No se detectaron rostros en una o ambas imágenes",
                    "verification_score": 0.0,
                    "is_match": False
                }
            
            # Calcular distancia entre encodings
            distance = face_recognition.face_distance([doc_encoding], live_encoding)[0]
            
            # Convertir distancia a score (0-1, donde 1 es perfecto match)
            verification_score = 1.0 - distance
            
            # Umbral de aceptación (0.6 = 60% de similitud)
            is_match = verification_score >= 0.6
            
            return {
                "success": True,
                "verification_score": round(verification_score, 3),
                "is_match": is_match,
                "distance": round(distance, 3)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "verification_score": 0.0,
                "is_match": False
            }
    
    @staticmethod
    def _get_face_encoding(image_data: str) -> Optional[np.ndarray]:
        """
        Extrae el encoding facial de una imagen
        """
        try:
            # Decodificar imagen base64
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convertir a numpy array
            image_array = np.array(image)
            
            # Detectar rostros y obtener encodings
            face_encodings = face_recognition.face_encodings(image_array)
            
            if len(face_encodings) > 0:
                return face_encodings[0]  # Retornar el primer rostro detectado
            else:
                return None
                
        except Exception as e:
            print(f"Error procesando imagen: {e}")
            return None
    
    @staticmethod
    def validate_image_quality(image_data: str) -> Dict[str, any]:
        """
        Valida la calidad de una imagen para reconocimiento facial
        """
        try:
            # Decodificar imagen
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Verificar si hay rostros
            image_array = np.array(image)
            face_locations = face_recognition.face_locations(image_array)
            
            quality_score = 0.0
            issues = []
            
            if len(face_locations) == 0:
                issues.append("No se detectó ningún rostro")
            elif len(face_locations) > 1:
                issues.append("Se detectaron múltiples rostros")
            else:
                quality_score = 0.8  # Base score si hay un rostro
                
                # Verificar tamaño de la imagen
                width, height = image.size
                if width < 200 or height < 200:
                    issues.append("Imagen muy pequeña")
                    quality_score -= 0.2
                
                # Verificar si la imagen está muy oscura o muy clara
                gray_image = image.convert('L')
                avg_brightness = np.mean(gray_image)
                if avg_brightness < 50:
                    issues.append("Imagen muy oscura")
                    quality_score -= 0.3
                elif avg_brightness > 200:
                    issues.append("Imagen muy clara")
                    quality_score -= 0.3
            
            return {
                "success": True,
                "quality_score": max(0.0, quality_score),
                "face_count": len(face_locations),
                "issues": issues,
                "is_suitable": quality_score >= 0.5
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "quality_score": 0.0,
                "is_suitable": False
            } 