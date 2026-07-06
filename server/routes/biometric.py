from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from ..database import get_session
from ..models.facial_verification import FacialVerification
from ..schemas.facial_verification import FacialVerificationCreate, FacialVerificationRead
from ..middleware.auth_middleware import get_current_active_user
from ..services.ocr_service import OCRService
from ..services.facial_recognition import FacialRecognitionService
from typing import List
import base64

router = APIRouter(prefix="/biometric", tags=["biometric"])

@router.post("/ocr/process")
def process_document_ocr(
    image_data: str,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_active_user)
):
    """
    Procesa una imagen de documento usando OCR
    """
    try:
        result = OCRService.extract_text_from_image(image_data)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=f"Error en OCR: {result['error']}")
        
        # Verificar score mínimo (70%)
        if result["confidence_score"] < 0.7:
            return {
                "success": False,
                "message": "La calidad de la imagen no es suficiente para extraer información confiable",
                "confidence_score": result["confidence_score"],
                "min_required": 0.7
            }
        
        return {
            "success": True,
            "extracted_data": result["extracted_data"],
            "confidence_score": result["confidence_score"],
            "raw_text": result["raw_text"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando documento: {str(e)}")

@router.post("/facial/verify")
def verify_facial_identity(
    document_photo: str,
    live_photo: str,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_active_user)
):
    """
    Verifica identidad facial comparando foto de documento con foto en vivo
    """
    try:
        # Validar calidad de las imágenes
        doc_quality = FacialRecognitionService.validate_image_quality(document_photo)
        live_quality = FacialRecognitionService.validate_image_quality(live_photo)
        
        if not doc_quality["is_suitable"]:
            raise HTTPException(status_code=400, detail=f"Calidad de foto de documento insuficiente: {', '.join(doc_quality['issues'])}")
        
        if not live_quality["is_suitable"]:
            raise HTTPException(status_code=400, detail=f"Calidad de foto en vivo insuficiente: {', '.join(live_quality['issues'])}")
        
        # Comparar rostros
        comparison_result = FacialRecognitionService.compare_faces(document_photo, live_photo)
        
        if not comparison_result["success"]:
            raise HTTPException(status_code=400, detail=f"Error en comparación facial: {comparison_result['error']}")
        
        # Guardar resultado en base de datos
        verification_data = FacialVerificationCreate(
            userId=current_user.id,
            documentPhotoUrl=document_photo[:100] + "..." if len(document_photo) > 100 else document_photo,  # Guardar referencia
            livePhotoUrl=live_photo[:100] + "..." if len(live_photo) > 100 else live_photo,
            verificationScore=comparison_result["verification_score"],
            isValid=comparison_result["is_match"]
        )
        
        new_verification = FacialVerification(**verification_data.dict())
        session.add(new_verification)
        session.commit()
        session.refresh(new_verification)
        
        return {
            "success": True,
            "verification_score": comparison_result["verification_score"],
            "is_match": comparison_result["is_match"],
            "verification_id": new_verification.id,
            "quality_analysis": {
                "document_photo": doc_quality,
                "live_photo": live_quality
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en verificación facial: {str(e)}")

@router.get("/verifications", response_model=List[FacialVerificationRead])
def list_verifications(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_active_user)
):
    """
    Lista las verificaciones faciales del usuario
    """
    if current_user.profileId == 1:
        return session.exec(select(FacialVerification)).all()
    return session.exec(select(FacialVerification).where(FacialVerification.userId == current_user.id)).all()

@router.get("/verifications/{verification_id}", response_model=FacialVerificationRead)
def get_verification(
    verification_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_active_user)
):
    """
    Obtiene una verificación facial específica
    """
    verification = session.get(FacialVerification, verification_id)
    if not verification:
        raise HTTPException(status_code=404, detail="Verificación no encontrada")
    
    if current_user.profileId != 1 and verification.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver esta verificación")
    
    return verification 