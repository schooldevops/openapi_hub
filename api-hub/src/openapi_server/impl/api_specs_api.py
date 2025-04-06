# coding: utf-8

from typing import List, Dict, Any
from api_hub.apis.api_specs_api_base import BaseAPISpecsApi
from api_hub.models.api_spec import APISpec
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from api_hub.db.database import DatabaseSessionManager, get_db, Base

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, BigInteger, JSON
from sqlalchemy.ext.declarative import declarative_base
import json
from openapi_server.utils.util import safe_json_dumps, parse_json_content

class APISpecDB(declarative_base()):
    """
    API 스펙 데이터베이스 모델 클래스
    schema.sql의 api_specs 테이블 구조를 따름
    """
    __tablename__ = 'api_specs'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='API 스펙 아이디')
    project_id = Column(BigInteger, nullable=False, comment='프로젝트 아이디')
    version = Column(String(50), nullable=False, comment='API 스펙 버전')
    title = Column(String(100), nullable=False, comment='API 스펙 제목')
    description = Column(String(500), nullable=True, comment='API 스펙 설명')
    spec_content = Column(Text, nullable=False, comment='API 스펙 내용 (JSON 형식)')
    is_archived = Column(Boolean, default=False, comment='API 스펙 삭제 여부')
    access_role = Column(String(50), nullable=True, comment='API 접근 권한')
    created_by = Column(BigInteger, comment='API 스펙 생성자 아이디')
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment='API 스펙 생성일')
    updated_by = Column(BigInteger, comment='API 스펙 수정자 아이디')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='API 스펙 수정일')

    def toAPISpec(self):
        """
        데이터베이스 모델을 API 모델로 변환
        
        Returns:
            APISpec: API 모델 객체
        """
        # 저장된 spec_content는 JSON 문자열이므로 파싱
        parsed_content = parse_json_content(self.spec_content)
        
        print("---------------:::", self.spec_content)

        return APISpec(
            id=self.id,
            project_id=self.project_id,
            version=self.version,
            title=self.title,
            description=self.description,
            spec_content=parsed_content,
            is_archived=self.is_archived,
            access_role=self.access_role,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_by=self.updated_by,
            updated_at=self.updated_at
        )
    def toAPISpecDB(self, api_spec: APISpec):
        """
        데이터베이스 모델을 API 모델로 변환
        
        Returns:
            APISpec: API 모델 객체
        """ 

        print("---------------:::", api_spec)
        return APISpecDB(
            project_id=api_spec.project_id,
            version=api_spec.version,
            title=api_spec.title,
            description=api_spec.description,
            spec_content=api_spec.spec_content,
            is_archived=api_spec.is_archived,
            access_role=api_spec.access_role,
            created_by=api_spec.created_by,
            created_at=api_spec.created_at,
            updated_by=api_spec.updated_by,
            updated_at=api_spec.updated_at
        )   
    
class APISpecsApiImpl(BaseAPISpecsApi):
    """
    API Specs API 구현 클래스
    BaseAPISpecsApi를 상속받아 API 스펙 관련 API 엔드포인트를 구현합니다.
    """

    async def api_specs_get(self) -> List[APISpec]:
        """
        모든 API 스펙 목록을 반환하는 메서드
        
        Returns:
            List[APISpec]: API 스펙 객체 리스트
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 모든 API 스펙 반환 (삭제되지 않은 API 스펙만)
            api_specs = db.query(APISpecDB).filter(APISpecDB.is_archived == False).all() if db else []
            return [api_spec.toAPISpec() for api_spec in api_specs]

    async def api_specs_post(self, api_spec: APISpec) -> APISpec:
        """
        새 API 스펙을 생성하는 메서드
        
        Args:
            api_spec (APISpec): 생성할 API 스펙 정보
            
        Returns:
            APISpec: 생성된 API 스펙 정보
        """
        print("--------------- 1111 :::", api_spec)
        with DatabaseSessionManager() as db:
            # spec_content를 JSON 형식으로 변환 (유틸리티 함수 사용)
            spec_content = safe_json_dumps(api_spec.spec_content)

            # 새 API 스펙 객체 생성
            new_api_spec_db = APISpecDB(
                project_id=api_spec.project_id,
                version=api_spec.version,
                title=api_spec.title,
                description=api_spec.description,
                spec_content=spec_content,  # JSON 문자열로 변환된 content
                is_archived=False,
                access_role=api_spec.access_role,
                created_by=api_spec.created_by,
                created_at=datetime.now(),
                updated_by=api_spec.created_by,  # 생성 시 수정자도 동일하게 설정
                updated_at=datetime.now()
            )
            
            # 데이터베이스에 API 스펙 추가
            db.add(new_api_spec_db)
            db.commit()
            db.refresh(new_api_spec_db)
            
            # 생성된 API 스펙 정보 반환
            return new_api_spec_db.toAPISpec()

    async def api_specs_api_spec_id_get(self, api_spec_id: int) -> APISpec:
        """
        특정 ID의 API 스펙 정보를 조회하는 메서드
        
        Args:
            api_spec_id (int): 조회할 API 스펙 ID
            
        Returns:
            APISpec: 조회된 API 스펙 정보
            
        Raises:
            HTTPException: API 스펙이 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 API 스펙 조회 (삭제되지 않은 API 스펙만)
            api_spec_db = db.query(APISpecDB).filter(
                APISpecDB.id == api_spec_id,
                APISpecDB.is_archived == False
            ).first()
            
            # API 스펙이 존재하지 않으면 404 에러 발생
            if api_spec_db is None:
                raise HTTPException(status_code=404, detail=f"API Spec with ID {api_spec_id} not found")
            
            # 조회된 API 스펙 정보 반환
            return api_spec_db.toAPISpec()

    async def api_specs_api_spec_id_put(self, api_spec_id: int, api_spec: APISpec) -> APISpec:
        """
        특정 ID의 API 스펙 정보를 업데이트하는 메서드
        
        Args:
            api_spec_id (int): 업데이트할 API 스펙 ID
            api_spec (APISpec): 업데이트할 API 스펙 정보
            
        Returns:
            APISpec: 업데이트된 API 스펙 정보
            
        Raises:
            HTTPException: API 스펙이 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 API 스펙 조회 (삭제되지 않은 API 스펙만)
            api_spec_db = db.query(APISpecDB).filter(
                APISpecDB.id == api_spec_id,
                APISpecDB.is_archived == False
            ).first()
            
            # API 스펙이 존재하지 않으면 404 에러 발생
            if api_spec_db is None:
                raise HTTPException(status_code=404, detail=f"API Spec with ID {api_spec_id} not found")
            
            # API 스펙 정보 업데이트
            api_spec_db.project_id = api_spec.project_id if api_spec.project_id else api_spec_db.project_id
            api_spec_db.version = api_spec.version if api_spec.version else api_spec_db.version
            api_spec_db.title = api_spec.title if api_spec.title else api_spec_db.title
            api_spec_db.description = api_spec.description if api_spec.description is not None else api_spec_db.description
            
            # spec_content가 제공된 경우 JSON 형식으로 변환하여 저장
            if api_spec.spec_content is not None:
                api_spec_db.spec_content = safe_json_dumps(api_spec.spec_content)
                
            api_spec_db.access_role = api_spec.access_role if api_spec.access_role is not None else api_spec_db.access_role
            api_spec_db.updated_by = api_spec.updated_by if api_spec.updated_by else api_spec_db.updated_by
            api_spec_db.updated_at = datetime.now()
            
            # 변경사항 커밋
            db.commit()
            db.refresh(api_spec_db)
            
            # 업데이트된 API 스펙 정보 반환
            return api_spec_db.toAPISpec()

    async def api_specs_api_spec_id_delete(self, api_spec_id: int) -> None:
        """
        특정 ID의 API 스펙을 삭제하는 메서드 (논리적 삭제 - is_archived 플래그 설정)
        
        Args:
            api_spec_id (int): 삭제할 API 스펙 ID
            
        Raises:
            HTTPException: API 스펙이 존재하지 않을 경우
        """
        with DatabaseSessionManager() as db:
            # 데이터베이스에서 API 스펙 조회 (삭제되지 않은 API 스펙만)
            api_spec_db = db.query(APISpecDB).filter(
                APISpecDB.id == api_spec_id,
                APISpecDB.is_archived == False
            ).first()
            
            # API 스펙이 존재하지 않으면 404 에러 발생
            if api_spec_db is None:
                raise HTTPException(status_code=404, detail=f"API Spec with ID {api_spec_id} not found")
            
            # API 스펙 논리적 삭제 (is_archived 플래그 설정)
            api_spec_db.is_archived = True
            api_spec_db.updated_at = datetime.now()
            
            # 변경사항 커밋
            db.commit()
