from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.nationality import Nationality
from ..schemas.nationality import NationalityCreate, NationalityRead
from ..middleware.auth_middleware import get_current_active_user
from typing import List

router = APIRouter(prefix="/nationalities", tags=["nationalities"])

@router.get("/", response_model=List[NationalityRead])
def list_nationalities(session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a esta información")
    return session.exec(select(Nationality)).all()

@router.post("/", response_model=NationalityRead)
def create_nationality(nationality: NationalityCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear nacionalidades")
    new_nationality = Nationality(**nationality.dict())
    session.add(new_nationality)
    session.commit()
    session.refresh(new_nationality)
    return new_nationality

@router.get("/{nationality_id}", response_model=NationalityRead)
def get_nationality(nationality_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    nationality = session.get(Nationality, nationality_id)
    if not nationality:
        raise HTTPException(status_code=404, detail="Nacionalidad no encontrada")
    return nationality

@router.put("/{nationality_id}", response_model=NationalityRead)
def update_nationality(nationality_id: int, nationality: NationalityCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar nacionalidades")
    db_nationality = session.get(Nationality, nationality_id)
    if not db_nationality:
        raise HTTPException(status_code=404, detail="Nacionalidad no encontrada")
    for key, value in nationality.dict().items():
        setattr(db_nationality, key, value)
    session.add(db_nationality)
    session.commit()
    session.refresh(db_nationality)
    return db_nationality

@router.delete("/{nationality_id}")
def delete_nationality(nationality_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar nacionalidades")
    db_nationality = session.get(Nationality, nationality_id)
    if not db_nationality:
        raise HTTPException(status_code=404, detail="Nacionalidad no encontrada")
    session.delete(db_nationality)
    session.commit()
    return {"ok": True} 