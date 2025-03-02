from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """
    사용자 기본 정보를 정의하는 Pydantic 모델
    
    Attributes:
        email (EmailStr): 사용자 이메일
        username (str): 사용자 이름
    """
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """
    사용자 생성 시 필요한 정보를 정의하는 Pydantic 모델
    
    Attributes:
        password (str): 사용자 비밀번호
    """
    password: str

class UserUpdate(BaseModel):
    """
    사용자 정보 업데이트 시 필요한 정보를 정의하는 Pydantic 모델
    
    Attributes:
        email (Optional[EmailStr]): 사용자 이메일 (선택)
        username (Optional[str]): 사용자 이름 (선택)
        password (Optional[str]): 사용자 비밀번호 (선택)
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    """
    데이터베이스에 저장된 사용자 정보를 표현하는 Pydantic 모델
    
    Attributes:
        id (int): 사용자 고유 식별자
        created_at (datetime): 계정 생성 시간
        updated_at (datetime): 계정 정보 수정 시간
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 