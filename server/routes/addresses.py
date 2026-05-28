from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.address import Address
from ..schemas.address import AddressCreate, AddressRead
from ..middleware.auth_middleware import get_current_active_user
from typing import List

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/", response_model=List[AddressRead])
def list_addresses(session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId == 1:
        return session.exec(select(Address)).all()
    return session.exec(select(Address).where(Address.userId == current_user.id)).all()

@router.post("/", response_model=AddressRead)
def create_address(address: AddressCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1 and address.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear esta dirección")
    new_address = Address(**address.dict())
    session.add(new_address)
    session.commit()
    session.refresh(new_address)
    return new_address

@router.get("/{address_id}", response_model=AddressRead)
def get_address(address_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    address = session.get(Address, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    if current_user.profileId != 1 and address.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver esta dirección")
    return address

@router.put("/{address_id}", response_model=AddressRead)
def update_address(address_id: int, address: AddressCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    db_address = session.get(Address, address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    if current_user.profileId != 1 and db_address.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar esta dirección")
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    session.add(db_address)
    session.commit()
    session.refresh(db_address)
    return db_address

@router.delete("/{address_id}")
def delete_address(address_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    db_address = session.get(Address, address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    if current_user.profileId != 1 and db_address.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta dirección")
    session.delete(db_address)
    session.commit()
    return {"ok": True} 