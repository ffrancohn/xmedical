from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.center import Center
from ..schemas.center import CenterCreate, CenterRead
from ..middleware.auth_middleware import get_current_active_user
from typing import List

router = APIRouter(prefix="/centers", tags=["centers"])

@router.get("/", response_model=List[CenterRead])
def list_centers(session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a esta información")
    return session.exec(select(Center)).all()

@router.post("/", response_model=CenterRead)
def create_center(center: CenterCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear centros")
    new_center = Center(**center.dict())
    session.add(new_center)
    session.commit()
    session.refresh(new_center)
    return new_center

@router.get("/{center_id}", response_model=CenterRead)
def get_center(center_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    center = session.get(Center, center_id)
    if not center:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return center

@router.put("/{center_id}", response_model=CenterRead)
def update_center(center_id: int, center: CenterCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar centros")
    db_center = session.get(Center, center_id)
    if not db_center:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    for key, value in center.dict().items():
        setattr(db_center, key, value)
    session.add(db_center)
    session.commit()
    session.refresh(db_center)
    return db_center

@router.delete("/{center_id}")
def delete_center(center_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar centros")
    db_center = session.get(Center, center_id)
    if not db_center:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    session.delete(db_center)
    session.commit()
    return {"ok": True} 