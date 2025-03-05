# coding: utf-8

from typing import List, Dict, Any
from api_hub.apis.project_credentials_api_base import BaseProjectCredentialsApi
from api_hub.models.project_credential import ProjectCredential
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from api_hub.db.database import DatabaseSessionManager, get_db, Base

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import secrets

class ProjectCredentialDB(declarative_base()):
    """
    프로젝트 Credential 데이터베이스 모델 클래스
    schema.sql의 project_credentials 테이블 구조를 따름
    """
    __tablename__ = 'project_credentials'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='프로젝트 Credential 아이디')
    project_id = Column(BigInteger, comment='프로젝트 아이디')
    api_key_name = Column(String(255), nullable=False, comment='API 키 이름')
    api_key = Column(String(255), nullable=False, comment='API 키')
    api_secret = Column(String(255), nullable=False, comment='API 시크릿')
    created_by = Column(BigInteger, comment='API 문서 생성자 아이디')
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment='프로젝트 Credential 생성일')
    expires_at = Column(DateTime, default=lambda: datetime.now() + timedelta(days=90), nullable=False, comment='프로젝트 Credential 만료일 기본 90일')

    def toProjectCredential(self):
        """
        데이터베이스 모델을 API 모델로 변환
        
        Returns:
            ProjectCredential: API 모델 객체
        """
        return ProjectCredential(
            id=self.id,
            project_id=self.project_id,
            api_key_name=self.api_key_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            created_by=self.created_by,
            created_at=self.created_at,
            expires_at=self.expires_at
        )
    
    def toProjectCredentialDB(self, project_credential: ProjectCredential):
        """
        프로젝트 Credential API 모델을 데이터베이스 모델로 변환
        
        Args:
            project_credential (ProjectCredential): 변환할 프로젝트 Credential 정보
        """
        return ProjectCredentialDB(
            project_id=project_credential.project_id,
            api_key_name=project_credential.api_key_name,
            api_key=project_credential.api_key,
            api_secret=project_credential.api_secret,
            created_by=project_credential.created_by,
            created_at=project_credential.created_at,
            expires_at=project_credential.expires_at
        )   
    

class ProjectCredentialsApi(BaseProjectCredentialsApi):
    """
    프로젝트 Credential API 구현 클래스
    BaseProjectCredentialsApi를 상속받아 구현
    """

    async def project_credentials_get(self) -> List[ProjectCredential]:
        """
        모든 프로젝트 Credential 목록을 반환하는 메서드
        
        Returns:
            List[ProjectCredential]: 프로젝트 Credential 객체 리스트
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 모든 프로젝트 Credential 조회
            credentials = db.query(ProjectCredentialDB).all()
            
            # 조회된 프로젝트 Credential을 API 모델로 변환하여 반환
            return [credential.toProjectCredential() for credential in credentials]

    async def project_credentials_post(self, project_credential: ProjectCredential) -> ProjectCredential:
        """
        새 프로젝트 Credential을 생성하는 메서드
        
        Args:
            project_credential (ProjectCredential): 생성할 프로젝트 Credential 정보
            
        Returns:
            ProjectCredential: 생성된 프로젝트 Credential 정보
        """
        with DatabaseSessionManager() as db:
            # API 키와 시크릿 생성
            api_key = secrets.token_urlsafe(32)
            api_secret = secrets.token_urlsafe(64)
            
            # 만료일 설정 (기본 90일)
            expires_at = datetime.now() + timedelta(days=90)
            if project_credential.expires_at:
                expires_at = project_credential.expires_at
            
            # 새 프로젝트 Credential 객체 생성
            new_credential_db = ProjectCredentialDB(
                project_id=project_credential.project_id,
                api_key_name=project_credential.api_key_name,
                api_key=api_key,
                api_secret=api_secret,
                created_by=project_credential.created_by,
                created_at=datetime.now(),
                expires_at=expires_at
            )
            
            # 데이터베이스에 프로젝트 Credential 추가
            db.add(new_credential_db)
            db.commit()
            db.refresh(new_credential_db)
            
            # 생성된 프로젝트 Credential 정보 반환
            return new_credential_db.toProjectCredential()

    async def project_credentials_project_credential_id_delete(self, project_credential_id: int) -> None:
        """
        특정 프로젝트 Credential을 삭제하는 메서드
        
        Args:
            project_credential_id (int): 삭제할 프로젝트 Credential ID
            
        Raises:
            HTTPException: 프로젝트 Credential이 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 특정 프로젝트 Credential 조회
            credential = db.query(ProjectCredentialDB).filter(
                ProjectCredentialDB.id == project_credential_id
            ).first()
            
            # 프로젝트 Credential이 존재하지 않으면 404 에러 발생
            if credential is None:
                raise HTTPException(status_code=404, detail=f"Project Credential with ID {project_credential_id} not found")
            
            # 데이터베이스에서 프로젝트 Credential 삭제
            db.delete(credential)
            db.commit()

    async def project_credentials_project_credential_id_get(self, project_credential_id: int) -> ProjectCredential:
        """
        특정 프로젝트 Credential 정보를 반환하는 메서드
        
        Args:
            project_credential_id (int): 조회할 프로젝트 Credential ID
            
        Returns:
            ProjectCredential: 프로젝트 Credential 객체
            
        Raises:
            HTTPException: 프로젝트 Credential이 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 특정 프로젝트 Credential 조회
            credential = db.query(ProjectCredentialDB).filter(
                ProjectCredentialDB.id == project_credential_id
            ).first()
            
            # 프로젝트 Credential이 존재하지 않으면 404 에러 발생
            if credential is None:
                raise HTTPException(status_code=404, detail=f"Project Credential with ID {project_credential_id} not found")
            
            # 조회된 프로젝트 Credential을 API 모델로 변환하여 반환
            return credential.toProjectCredential()

    async def project_credentials_project_id_get(self, project_id: int) -> List[ProjectCredential]:
        """
        특정 프로젝트의 모든 Credential 목록을 반환하는 메서드
        
        Args:
            project_id (int): 조회할 프로젝트 ID
            
        Returns:
            List[ProjectCredential]: 프로젝트 Credential 객체 리스트
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 특정 프로젝트의 모든 Credential 조회
            credentials = db.query(ProjectCredentialDB).filter(
                ProjectCredentialDB.project_id == project_id
            ).all()
            
            # 조회된 프로젝트 Credential을 API 모델로 변환하여 반환
            return [credential.toProjectCredential() for credential in credentials]

    async def project_credentials_project_credential_id_put(self, project_credential_id: int, project_credential: ProjectCredential) -> ProjectCredential:
        """
        특정 프로젝트 Credential 정보를 업데이트하는 메서드
        
        Args:
            project_credential_id (int): 업데이트할 프로젝트 Credential ID
            project_credential (ProjectCredential): 업데이트할 프로젝트 Credential 정보
            
        Returns:
            ProjectCredential: 업데이트된 프로젝트 Credential 정보
            
        Raises:
            HTTPException: 프로젝트 Credential이 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 특정 프로젝트 Credential 조회
            credential = db.query(ProjectCredentialDB).filter(
                ProjectCredentialDB.id == project_credential_id
            ).first()
            
            # 프로젝트 Credential이 존재하지 않으면 404 에러 발생
            if credential is None:
                raise HTTPException(status_code=404, detail=f"Project Credential with ID {project_credential_id} not found")
            
            # 프로젝트 Credential 정보 업데이트
            if project_credential.expires_at:
                credential.expires_at = project_credential.expires_at
            
            # 변경사항 커밋
            db.commit()
            db.refresh(credential)
            
            # 업데이트된 프로젝트 Credential 정보 반환
            return credential.toProjectCredential()



