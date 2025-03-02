# coding: utf-8

from typing import List, Dict, Any
from api_hub.apis.users_api_base import BaseUsersApi
from api_hub.models.user import User
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from api_hub.db.database import DatabaseSessionManager, get_db

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

# 사용자 데이터를 저장할 임시 데이터베이스 (실제 구현에서는 데이터베이스 연결이 필요)
# users_db: Dict[int, User] = {}
# next_user_id = 1  # 사용자 ID 자동 증가를 위한 변수

class UsersDB(declarative_base()):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  

    def toUser(self):
        return User(id=self.id, email=self.email, full_name=self.full_name, password=self.password_hash, created_at=self.created_at, updated_at=self.updated_at)

    def toUserDB(self, user: User):
        return UsersDB(id=user.id, email=user.email, password_hash=user.password, full_name=user.full_name, created_at=user.created_at, updated_at=user.updated_at)  

class UsersApiImpl(BaseUsersApi):
    """
    Users API 구현 클래스
    BaseUsersApi를 상속받아 사용자 관련 API 엔드포인트를 구현합니다.
    """

    async def users_get(self, db: Session = Depends(get_db)) -> List[User]:
        """
        모든 사용자 목록을 반환하는 메서드
        
        Returns:
            List[User]: 사용자 객체 리스트
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 모든 사용자 반환
            users = db.query(UsersDB).all() if db else []
            print('------------- ::::', users)
            return [user.toUser() for user in users]

    async def users_post(self, user: User) -> User:
        """
        새 사용자를 생성하는 메서드
        
        Args:
            user (User): 생성할 사용자 정보
            
        Returns:
            User: 생성된 사용자 정보
        """
        global next_user_id
        
        # ID가 없으면 자동 할당
        # DatabaseSessionManager를 사용하여 데이터베이스 세션 생성
        with DatabaseSessionManager() as db:
            # 이미 존재하는 이메일인지 확인
            existing_user = db.query(UsersDB).filter(UsersDB.email == user.email).first()
            if existing_user:
                raise HTTPException(status_code=400, detail=f"User with email {user.email} already exists")
            
            # 새 사용자 객체 생성
            new_user_db = UsersDB(
                email=user.email,
                full_name=user.full_name,
                password_hash=user.password,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # 데이터베이스에 사용자 추가
            db.add(new_user_db)
            db.commit()
            db.refresh(new_user_db)
            
            # 생성된 사용자 정보 반환
            return new_user_db.toUser()

    async def users_user_id_get(self, user_id: int) -> User:
        """
        특정 ID의 사용자 정보를 조회하는 메서드
        
        Args:
            user_id (int): 조회할 사용자 ID
            
        Returns:
            User: 조회된 사용자 정보
            
        Raises:
            HTTPException: 사용자가 존재하지 않을 경우
        """
        # DatabaseSessionManager를 사용하여 데이터베이스 세션 생성
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 사용자 조회
            user_db = db.query(UsersDB).filter(UsersDB.id == user_id).first()
            
            # 사용자가 존재하지 않으면 404 에러 발생
            if user_db is None:
                raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
            
            # 조회된 사용자 정보 반환
            return user_db.toUser()

    async def users_user_id_put(self, user_id: int, user: User) -> User:
        """
        특정 ID의 사용자 정보를 업데이트하는 메서드
        
        Args:
            user_id (int): 업데이트할 사용자 ID
            user (User): 업데이트할 사용자 정보
            
        Returns:
            User: 업데이트된 사용자 정보
            
        Raises:
            HTTPException: 사용자가 존재하지 않을 경우
        """
        # DatabaseSessionManager를 사용하여 데이터베이스 세션 생성
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 사용자 조회
            user_db = db.query(UsersDB).filter(UsersDB.id == user_id).first()
            
            # 사용자가 존재하지 않으면 404 에러 발생
            if user_db is None:
                raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
            
            # 사용자 정보 업데이트
            user_db.email = user.email if user.email else user_db.email
            user_db.full_name = user.full_name if user.full_name else user_db.full_name
            
            # 비밀번호가 제공된 경우 해시하여 저장
            if user.password:
                user_db.password_hash = (user.password)
                
            user_db.updated_at = datetime.now()
            
            # 변경사항 커밋
            db.commit()
            db.refresh(user_db)
            
            # 업데이트된 사용자 정보 반환
            return user_db.toUser()

    async def users_user_id_delete(self, user_id: int) -> None:
        """
        특정 ID의 사용자를 삭제하는 메서드
        
        Args:
            user_id (int): 삭제할 사용자 ID
            
        Raises:
            HTTPException: 사용자가 존재하지 않을 경우
        """
        # DatabaseSessionManager를 사용하여 데이터베이스 세션 생성
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 사용자 조회
            user_db = db.query(UsersDB).filter(UsersDB.id == user_id).first()
            
            # 사용자가 존재하지 않으면 404 에러 발생
            if user_db is None:
                raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
            
            # 사용자 삭제
            db.delete(user_db)
            
            # 변경사항 커밋
            db.commit()
