from datetime import datetime, timezone, timedelta
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Otp, Users
from app.oauth2 import create_access_token
from app.schemas import token


router = APIRouter(
    # prefix="/user"
    tags=["otp"]
)

@router.post("/verify_otp"  )
def verify_otp(user_data:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == user_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials !!")
    
    otp_data = db.query(Otp).filter(Otp.user_id == user.id).first()

    if (int(user_data.password) == otp_data.otp_number) and (datetime.now(timezone.utc) - otp_data.created_at) <= timedelta(minutes=2):
        token = create_access_token({"user_id" : user.id})
        return {"access_token": token, "token_type":"bearer"}
    return {"detail": "not verified"}
