from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.sql.expression import null
from app.database import Base


class Users(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

class Otp(Base):
    __tablename__= "otp"

    id = Column(Integer, primary_key=True, nullable=False)
    otp_number = Column(Integer, nullable = False)
    user_id = Column(Integer, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))