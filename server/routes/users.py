from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.user import User
from ..schemas.user import UserRead
from ..middleware.auth_middleware import get_current_active_user
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
def list_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)):
    # Solo administradores pueden listar todos los usuarios
    if current_user.profileId != 1:  # Asumiendo que profileId 1 es Administrador
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a esta información")
    
    users = session.exec(select(User)).all()
    return users

@router.get("/me", response_model=UserRead)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user 