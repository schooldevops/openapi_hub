# coding: utf-8

from typing import List, Dict, Any
from api_hub.apis.projects_api_base import BaseProjectsApi
from api_hub.models.project import Project
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from api_hub.db.database import DatabaseSessionManager, get_db, Base

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base

class ProjectDB(declarative_base()):
    """
    프로젝트 데이터베이스 모델 클래스
    schema.sql의 projects 테이블 구조를 따름
    """
    __tablename__ = 'projects'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='프로젝트 아이디')
    name = Column(String(100), nullable=False, comment='프로젝트 이름')
    description = Column(String(500), nullable=True, comment='프로젝트 설명')
    is_archived = Column(Boolean, default=False, comment='프로젝트 삭제 여부')
    created_by = Column(BigInteger, comment='프로젝트 생성자 아이디')
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment='프로젝트 생성일')
    updated_by = Column(BigInteger, comment='프로젝트 수정자 아이디')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='프로젝트 수정일')

    # creator = relationship("UserDB", foreign_keys=[created_by])
    # updator = relationship("UserDB", foreign_keys=[updated_by])

    def toProject(self):
        """
        데이터베이스 모델을 API 모델로 변환
        
        Returns:
            Project: API 모델 객체
        """
        return Project(
            id=self.id, 
            name=self.name, 
            description=self.description, 
            is_archived=self.is_archived,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_by=self.updated_by,
            updated_at=self.updated_at
        )
    
    def toProjectDB(self, project: Project):
        return ProjectDB(
            id=project.id,
            name=project.name,
            description=project.description,
            is_archived=project.is_archived,
            created_by=project.created_by,
            created_at=project.created_at,
            updated_by=project.updated_by,
            updated_at=project.updated_at
        )

class ProjectApiImpl(BaseProjectsApi):
    """
    Project API 구현 클래스
    BaseProjectApi를 상속받아 프로젝트 관련 API 엔드포인트를 구현합니다.
    """

    async def projects_get(self) -> List[Project]:
        """
        모든 프로젝트 목록을 반환하는 메서드
        
        Returns:
            List[Project]: 프로젝트 객체 리스트
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 모든 프로젝트 반환 (삭제되지 않은 프로젝트만)
            projects = db.query(ProjectDB).filter(ProjectDB.is_archived == False).all() if db else []
            return [project.toProject() for project in projects]

    async def projects_post(self, project: Project) -> Project:
        """
        새 프로젝트를 생성하는 메서드
        
        Args:
            project (Project): 생성할 프로젝트 정보
            
        Returns:
            Project: 생성된 프로젝트 정보
        """
        with DatabaseSessionManager() as db:
            # 새 프로젝트 객체 생성
            new_project_db = ProjectDB(
                name=project.name,
                description=project.description,
                is_archived=False,
                created_by=project.created_by,
                created_at=datetime.now(),
                updated_by=project.created_by,  # 생성 시 수정자도 동일하게 설정
                updated_at=datetime.now()
            )
            
            # 데이터베이스에 프로젝트 추가
            db.add(new_project_db)
            db.commit()
            db.refresh(new_project_db)
            
            # 생성된 프로젝트 정보 반환
            return new_project_db.toProject()

    async def projects_project_id_get(self, project_id: int) -> Project:
        """
        특정 ID의 프로젝트 정보를 조회하는 메서드
        
        Args:
            project_id (int): 조회할 프로젝트 ID
            
        Returns:
            Project: 조회된 프로젝트 정보
            
        Raises:
            HTTPException: 프로젝트가 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 프로젝트 조회 (삭제되지 않은 프로젝트만)
            project_db = db.query(ProjectDB).filter(
                ProjectDB.id == project_id,
                ProjectDB.is_archived == False
            ).first()
            
            # 프로젝트가 존재하지 않으면 404 에러 발생
            if project_db is None:
                raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
            
            # 조회된 프로젝트 정보 반환
            return project_db.toProject()

    async def projects_project_id_put(self, project_id: int, project: Project) -> Project:
        """
        특정 ID의 프로젝트 정보를 업데이트하는 메서드
        
        Args:
            project_id (int): 업데이트할 프로젝트 ID
            project (Project): 업데이트할 프로젝트 정보
            
        Returns:
            Project: 업데이트된 프로젝트 정보
            
        Raises:
            HTTPException: 프로젝트가 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 프로젝트 조회 (삭제되지 않은 프로젝트만)
            project_db = db.query(ProjectDB).filter(
                ProjectDB.id == project_id,
                ProjectDB.is_archived == False
            ).first()
            
            # 프로젝트가 존재하지 않으면 404 에러 발생
            if project_db is None:
                raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
            
            # 프로젝트 정보 업데이트
            project_db.name = project.name if project.name else project_db.name
            project_db.description = project.description if project.description is not None else project_db.description
            project_db.updated_by = project.updated_by if project.updated_by else project_db.updated_by
            project_db.updated_at = datetime.now()
            
            # 변경사항 커밋
            db.commit()
            db.refresh(project_db)
            
            # 업데이트된 프로젝트 정보 반환
            return project_db.toProject()

    async def projects_project_id_delete(self, project_id: int) -> None:
        """
        특정 ID의 프로젝트를 삭제하는 메서드 (논리적 삭제 - is_archived 플래그 설정)
        
        Args:
            project_id (int): 삭제할 프로젝트 ID
            
        Raises:
            HTTPException: 프로젝트가 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 프로젝트 조회 (삭제되지 않은 프로젝트만)
            project_db = db.query(ProjectDB).filter(
                ProjectDB.id == project_id,
                ProjectDB.is_archived == False
            ).first()
            
            # 프로젝트가 존재하지 않으면 404 에러 발생
            if project_db is None:
                raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
            
            # 프로젝트 논리적 삭제 (is_archived 플래그 설정)
            project_db.is_archived = True
            project_db.updated_at = datetime.now()
            
            # 변경사항 커밋
            db.commit()


