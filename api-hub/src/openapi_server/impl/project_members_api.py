# coding: utf-8

from typing import List, Dict, Any
from api_hub.apis.project_members_api_base import BaseProjectMembersApi
from api_hub.models.project_member import ProjectMember
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from api_hub.db.database import DatabaseSessionManager, get_db, Base

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

class ProjectMemberDB(declarative_base()):
    """
    프로젝트 멤버 데이터베이스 모델 클래스
    schema.sql의 project_members 테이블 구조를 따름
    """
    __tablename__ = 'project_members'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='프로젝트 멤버 아이디')
    project_id = Column(BigInteger, comment='프로젝트 아이디')
    user_id = Column(BigInteger, comment='사용자 아이디')
    member_role = Column(String(20), nullable=False, comment='프로젝트 멤버 역할')
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment='프로젝트 멤버 생성일')

    # project = relationship("ProjectDB", foreign_keys=[project_id])
    # user = relationship("UserDB", foreign_keys=[user_id])

    def toProjectMember(self):
        """
        데이터베이스 모델을 API 모델로 변환
        
        Returns:
            ProjectMember: API 모델 객체
        """
        return ProjectMember(
            id=self.id,
            project_id=self.project_id,
            user_id=self.user_id,
            member_role=self.member_role,
            created_at=self.created_at
        )

    def toProjectMemberDB(self, project_member: ProjectMember):
        return ProjectMemberDB(
            id=project_member.id,
            project_id=project_member.project_id,
            user_id=project_member.user_id,
            member_role=project_member.member_role, 
            created_at=project_member.created_at
        )

class ProjectMemberApiImpl(BaseProjectMembersApi):
    """
    ProjectMember API 구현 클래스
    BaseProjectMembersApi를 상속받아 프로젝트 멤버 관련 API 엔드포인트를 구현합니다.
    """

    async def project_members_get(self) -> List[ProjectMember]:
        """
        모든 프로젝트 멤버 목록을 반환하는 메서드
        
        Returns:
            List[ProjectMember]: 프로젝트 멤버 객체 리스트
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 모든 프로젝트 멤버 반환
            project_members = db.query(ProjectMemberDB).all() if db else []
            return [member.toProjectMember() for member in project_members]

    async def project_members_post(self, project_member: ProjectMember) -> ProjectMember:
        """
        새 프로젝트 멤버를 생성하는 메서드
        
        Args:
            project_member (ProjectMember): 생성할 프로젝트 멤버 정보
            
        Returns:
            ProjectMember: 생성된 프로젝트 멤버 정보
        """
        with DatabaseSessionManager() as db:
            # 이미 존재하는 프로젝트 멤버인지 확인
            existing_member = db.query(ProjectMemberDB).filter(
                ProjectMemberDB.project_id == project_member.project_id,
                ProjectMemberDB.user_id == project_member.user_id
            ).first()
            
            if existing_member:
                raise HTTPException(status_code=400, detail="User is already a member of this project")
            
            # 새 프로젝트 멤버 객체 생성
            new_member_db = ProjectMemberDB(
                project_id=project_member.project_id,
                user_id=project_member.user_id,
                member_role=project_member.member_role,
                created_at=datetime.now()
            )

            print("--------- new projet member db ::::", new_member_db.project_id, new_member_db.user_id, new_member_db.member_role, new_member_db.created_at)
            
            # 데이터베이스에 프로젝트 멤버 추가
            db.add(new_member_db)
            db.commit()
            db.refresh(new_member_db)
            
            # 생성된 프로젝트 멤버 정보 반환
            return new_member_db.toProjectMember()

    async def project_members_project_member_id_get(self, project_member_id: int) -> ProjectMember:
        """
        특정 프로젝트의 모든 멤버 목록을 반환하는 메서드
        
        Args:
            project_id (int): 조회할 프로젝트 ID
            
        Returns:
            List[ProjectMember]: 프로젝트 멤버 객체 리스트
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 특정 프로젝트의 모든 멤버 조회
            project_members = db.query(ProjectMemberDB).filter(
                ProjectMemberDB.id == project_member_id
            ).first()
            
            return project_members.toProjectMember()

    async def project_members_project_member_id_put(self, project_member_id: int, project_member: ProjectMember) -> ProjectMember:
        """
        특정 프로젝트의 특정 사용자 멤버 정보를 업데이트하는 메서드
        
        Args:
            project_id (int): 업데이트할 프로젝트 ID
            user_id (int): 업데이트할 사용자 ID
            project_member (ProjectMember): 업데이트할 프로젝트 멤버 정보
            
        Returns:
            ProjectMember: 업데이트된 프로젝트 멤버 정보
            
        Raises:
            HTTPException: 프로젝트 멤버가 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 특정 프로젝트의 특정 사용자 멤버 조회
            member_db = db.query(ProjectMemberDB).filter(
                ProjectMemberDB.id == project_member_id
            ).first()
            
            # 프로젝트 멤버가 존재하지 않으면 404 에러 발생
            if member_db is None:
                raise HTTPException(status_code=404, detail=f"ProjectMember {project_member_id} is not a member of project {project_id}")
            
            # 프로젝트 멤버 정보 업데이트
            member_db.member_role = project_member.member_role if project_member.member_role else member_db.member_role
            
            # 변경사항 커밋
            db.commit()
            db.refresh(member_db)
            
            # 업데이트된 프로젝트 멤버 정보 반환
            return member_db.toProjectMember()

    async def project_members_project_id_user_id_delete(self, project_member_id: int) -> None:
        """
        특정 프로젝트의 특정 사용자 멤버를 삭제하는 메서드
        
        Args:
            project_id (int): 삭제할 프로젝트 ID
            user_id (int): 삭제할 사용자 ID
            
        Raises:
            HTTPException: 프로젝트 멤버가 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 특정 프로젝트의 특정 사용자 멤버 조회
            member_db = db.query(ProjectMemberDB).filter(
                ProjectMemberDB.id == project_member_id
            ).first()
            
            # 프로젝트 멤버가 존재하지 않으면 404 에러 발생
            if member_db is None:
                raise HTTPException(status_code=404, detail=f"ProjectMember {project_member_id} is not a member of project {project_member_id}")
            
            # 프로젝트 멤버 삭제
            db.delete(member_db)
            db.commit()
