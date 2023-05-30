from datetime import datetime, timezone
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.schemas import UserCreate, UserCreate_resp
from app.models import Otp, Users
from app.database import get_db
from app.utils import verify_Pass
from .. import utils
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv  
import os

load_dotenv()

router = APIRouter(
    # prefix="/user"
    tags=["user"]
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserCreate_resp)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = utils.Hash(new_user.password)
        new_user.password = hashed_password

        new_user = Users(**new_user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    
@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials !!")
    
    if not verify_Pass(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials !!")
    
    #otp generate
    otp = random.randint(1000, 9999)
    
    #gmail smtp connection for sending otp
    smtp_connection = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_connection.starttls()
    smtp_connection.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD')) 

    email = MIMEMultipart()
    email['From'] = 'darshan.kadiya.sa@gmail.com'
    email['To'] = user_credentials.username
    email['Subject'] = 'Your OTP generated'

    email.attach(MIMEText(f'Your OTP is {otp} and it is valid for 2 minute only', 'plain'))

    smtp_connection.sendmail('darshan.kadiya.sa@gmail.com', user_credentials.username, email.as_string())
    smtp_connection.quit() 

    #store otp to table named Otp or update if exists
    otp_for_update = db.query(Otp).filter(Otp.user_id == user.id)

    if not otp_for_update.first():
        #insert otp
        new_otp = Otp(**{"otp_number": otp, "user_id": user.id})
        db.add(new_otp)
        db.commit()
    
    otp_for_update.update({"otp_number": otp, "created_at": datetime.now(timezone.utc)}, synchronize_session=False)
    db.commit() 
    
    return {"detail": "OTP Sent"}
    
