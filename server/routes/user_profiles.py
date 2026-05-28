from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.user_profile import UserProfile
from ..schemas.user_profile import UserProfileCreate, UserProfileRead
from ..middleware.auth_middleware import get_current_active_user
from typing import List

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/", response_model=List[UserProfileRead])
def list_profiles(session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a esta información")
    return session.exec(select(UserProfile)).all()

@router.post("/", response_model=UserProfileRead)
def create_profile(profile: UserProfileCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear perfiles")
    new_profile = UserProfile(**profile.dict())
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)
    return new_profile

@router.get("/{profile_id}", response_model=UserProfileRead)
def get_profile(profile_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    profile = session.get(UserProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile

@router.put("/{profile_id}", response_model=UserProfileRead)
def update_profile(profile_id: int, profile: UserProfileCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar perfiles")
    db_profile = session.get(UserProfile, profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    for key, value in profile.dict().items():
        setattr(db_profile, key, value)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile

@router.delete("/{profile_id}")
def delete_profile(profile_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar perfiles")
    db_profile = session.get(UserProfile, profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    session.delete(db_profile)
    session.commit()
    return {"ok": True} 