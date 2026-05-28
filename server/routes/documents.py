from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.document import Document
from ..schemas.document import DocumentCreate, DocumentRead
from ..middleware.auth_middleware import get_current_active_user
from typing import List

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/", response_model=List[DocumentRead])
def list_documents(session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId == 1:
        return session.exec(select(Document)).all()
    return session.exec(select(Document).where(Document.userId == current_user.id)).all()

@router.post("/", response_model=DocumentRead)
def create_document(document: DocumentCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1 and document.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear este documento")
    new_document = Document(**document.dict())
    session.add(new_document)
    session.commit()
    session.refresh(new_document)
    return new_document

@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    document = session.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    if current_user.profileId != 1 and document.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver este documento")
    return document

@router.put("/{document_id}", response_model=DocumentRead)
def update_document(document_id: int, document: DocumentCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    db_document = session.get(Document, document_id)
    if not db_document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    if current_user.profileId != 1 and db_document.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar este documento")
    for key, value in document.dict().items():
        setattr(db_document, key, value)
    session.add(db_document)
    session.commit()
    session.refresh(db_document)
    return db_document

@router.delete("/{document_id}")
def delete_document(document_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    db_document = session.get(Document, document_id)
    if not db_document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    if current_user.profileId != 1 and db_document.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar este documento")
    session.delete(db_document)
    session.commit()
    return {"ok": True} 