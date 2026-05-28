from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.feedback import Feedback
from ..schemas.feedback import FeedbackCreate, FeedbackRead
from ..middleware.auth_middleware import get_current_active_user
from typing import List

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.get("/", response_model=List[FeedbackRead])
def list_feedback(session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId == 1:
        return session.exec(select(Feedback)).all()
    return session.exec(select(Feedback).where(Feedback.userId == current_user.id)).all()

@router.post("/", response_model=FeedbackRead)
def create_feedback(feedback: FeedbackCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    if current_user.profileId != 1 and feedback.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear este feedback")
    new_feedback = Feedback(**feedback.dict())
    session.add(new_feedback)
    session.commit()
    session.refresh(new_feedback)
    return new_feedback

@router.get("/{feedback_id}", response_model=FeedbackRead)
def get_feedback(feedback_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    feedback = session.get(Feedback, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")
    if current_user.profileId != 1 and feedback.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver este feedback")
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackRead)
def update_feedback(feedback_id: int, feedback: FeedbackCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    db_feedback = session.get(Feedback, feedback_id)
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")
    if current_user.profileId != 1 and db_feedback.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar este feedback")
    for key, value in feedback.dict().items():
        setattr(db_feedback, key, value)
    session.add(db_feedback)
    session.commit()
    session.refresh(db_feedback)
    return db_feedback

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    db_feedback = session.get(Feedback, feedback_id)
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")
    if current_user.profileId != 1 and db_feedback.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar este feedback")
    session.delete(db_feedback)
    session.commit()
    return {"ok": True} 