from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from ..db.database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserInDB

# 비밀번호 해싱을 위한 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# API 라우터 생성
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def get_password_hash(password: str) -> str:
    """
    비밀번호를 해시화하는 유틸리티 함수
    
    Args:
        password (str): 원본 비밀번호
        
    Returns:
        str: 해시화된 비밀번호
    """
    return pwd_context.hash(password)

@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자를 생성하는 엔드포인트
    
    Args:
        user (UserCreate): 생성할 사용자 정보
        db (Session): 데이터베이스 세션
        
    Returns:
        UserInDB: 생성된 사용자 정보
        
    Raises:
        HTTPException: 이메일이 이미 존재하는 경우
    """
    # 이메일 중복 체크
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 비밀번호 해시화
    hashed_password = get_password_hash(user.password)
    
    # 새 사용자 생성
    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자 정보를 조회하는 엔드포인트
    
    Args:
        user_id (int): 조회할 사용자 ID
        db (Session): 데이터베이스 세션
        
    Returns:
        UserInDB: 조회된 사용자 정보
        
    Raises:
        HTTPException: 사용자를 찾을 수 없는 경우
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.get("/", response_model=List[UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    사용자 목록을 조회하는 엔드포인트
    
    Args:
        skip (int): 건너뛸 레코드 수
        limit (int): 조회할 최대 레코드 수
        db (Session): 데이터베이스 세션
        
    Returns:
        List[UserInDB]: 사용자 목록
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.put("/{user_id}", response_model=UserInDB)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    사용자 정보를 업데이트하는 엔드포인트
    
    Args:
        user_id (int): 업데이트할 사용자 ID
        user (UserUpdate): 업데이트할 사용자 정보
        db (Session): 데이터베이스 세션
        
    Returns:
        UserInDB: 업데이트된 사용자 정보
        
    Raises:
        HTTPException: 사용자를 찾을 수 없는 경우
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 업데이트할 데이터 준비
    update_data = user.model_dump(exclude_unset=True)
    
    # 비밀번호가 포함된 경우 해시화
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    # 데이터 업데이트
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    사용자를 삭제하는 엔드포인트
    
    Args:
        user_id (int): 삭제할 사용자 ID
        db (Session): 데이터베이스 세션
        
    Raises:
        HTTPException: 사용자를 찾을 수 없는 경우
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(db_user)
    db.commit() 