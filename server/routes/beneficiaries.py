from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.beneficiary import Beneficiary
from ..schemas.beneficiary import BeneficiaryCreate, BeneficiaryRead
from ..middleware.auth_middleware import get_current_active_user
from typing import List

router = APIRouter(prefix="/beneficiaries", tags=["beneficiaries"])

@router.get("/", response_model=List[BeneficiaryRead])
def list_beneficiaries(session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId == 1:
        return session.exec(select(Beneficiary)).all()
    return session.exec(select(Beneficiary).where(Beneficiary.userId == current_user.id)).all()

@router.post("/", response_model=BeneficiaryRead)
def create_beneficiary(beneficiary: BeneficiaryCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1 and beneficiary.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear este beneficiario")
    new_beneficiary = Beneficiary(**beneficiary.dict())
    session.add(new_beneficiary)
    session.commit()
    session.refresh(new_beneficiary)
    return new_beneficiary

@router.get("/{beneficiary_id}", response_model=BeneficiaryRead)
def get_beneficiary(beneficiary_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    beneficiary = session.get(Beneficiary, beneficiary_id)
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    if current_user.profileId != 1 and beneficiary.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver este beneficiario")
    return beneficiary

@router.put("/{beneficiary_id}", response_model=BeneficiaryRead)
def update_beneficiary(beneficiary_id: int, beneficiary: BeneficiaryCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    db_beneficiary = session.get(Beneficiary, beneficiary_id)
    if not db_beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    if current_user.profileId != 1 and db_beneficiary.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar este beneficiario")
    for key, value in beneficiary.dict().items():
        setattr(db_beneficiary, key, value)
    session.add(db_beneficiary)
    session.commit()
    session.refresh(db_beneficiary)
    return db_beneficiary

@router.delete("/{beneficiary_id}")
def delete_beneficiary(beneficiary_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    db_beneficiary = session.get(Beneficiary, beneficiary_id)
    if not db_beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    if current_user.profileId != 1 and db_beneficiary.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar este beneficiario")
    session.delete(db_beneficiary)
    session.commit()
    return {"ok": True} 