from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Union, Any
from pydantic import BaseModel, EmailStr, Field, validator
from kafka import KafkaProducer
import json
from enum import Enum
import os
from dotenv import load_dotenv
import uuid

# 환경 변수 로드
load_dotenv()

# JWT 설정
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Kafka 설정
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "test.mykafkacluster.org:18092")
KAFKA_TOPIC_PREFIX = "smartylighting.streetlights.1.0.action"

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 인메모리 데이터 저장소 (실제 구현에서는 데이터베이스 사용)
users_db: Dict[str, dict] = {}
projects_db: Dict[str, dict] = {}
api_specs_db: Dict[str, dict] = {}

# Pydantic 모델
class Season(str, Enum):
    SUMMER = "SUMMER"
    WINTER = "WINTER"

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"

class AccessRole(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    RESTRICTED = "restricted"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    owner: UserResponse

    class Config:
        from_attributes = True

class ApiSpecBase(BaseModel):
    title: str
    description: Optional[str] = None
    version: str = "1.0.0"
    spec_content: Dict[str, Any]
    access_role: AccessRole = AccessRole.PRIVATE

    @validator('spec_content')
    def validate_spec_content(cls, v):
        """
        spec_content 필드의 유효성을 검사하고 적절한 형식으로 변환
        """
        try:
            # 문자열인 경우 JSON으로 변환 시도
            if isinstance(v, str):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    # 문자열을 JSON 객체로 변환
                    return {"content": v}
            # 딕셔너리가 아닌 경우 JSON 객체로 변환
            elif not isinstance(v, dict):
                return {"content": str(v)}
            return v
        except Exception as e:
            raise ValueError(f"Invalid spec_content format: {str(e)}")

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        # spec_content를 JSON 문자열로 변환
        if 'spec_content' in d:
            d['spec_content'] = json.dumps(d['spec_content'])
        return d

class ApiSpecCreate(ApiSpecBase):
    project_id: str

class ApiSpecResponse(ApiSpecBase):
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str
    is_archived: bool = False

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="User password")

class ProjectRegistrationRequest(BaseModel):
    project: ProjectCreate
    user: UserCreate

    class Config:
        json_schema_extra = {
            "example": {
                "project": {
                    "name": "City Center Lights",
                    "description": "Downtown area streetlight management",
                    "location": "City Center"
                },
                "user": {
                    "username": "citymanager",
                    "password": "secure123",
                    "email": "manager@city.com",
                    "full_name": "City Manager",
                    "role": "ADMIN"
                }
            }
        }

class ScheduleRequest(BaseModel):
    season: Season
    startTime: str  # HH:MM format
    endTime: str    # HH:MM format

# FastAPI 앱 초기화
app = FastAPI(title="Streetlight BFF Service")

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영환경에서는 구체적인 도메인을 지정해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kafka 프로듀서 초기화
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 사용자 인증 함수
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str) -> Optional[UserResponse]:
    if username in users_db:
        user_data = users_db[username].copy()
        # 비밀번호 해시는 응답에서 제외
        user_data.pop("hashed_password", None)
        return UserResponse(**user_data)
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# API 엔드포인트
@app.post("/auth/login", response_model=Token)
async def login(login_data: Union[OAuth2PasswordRequestForm, LoginRequest] = Depends()):
    """
    로그인 처리 - Form 데이터와 JSON 데이터 모두 지원
    """
    username = getattr(login_data, "username", None)
    password = getattr(login_data, "password", None)
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login data format"
        )
    
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    stored_password_hash = users_db[username]["hashed_password"]
    if not verify_password(password, stored_password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": username})
    return Token(access_token=access_token)

@app.post("/projects", status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
async def create_project(registration: ProjectRegistrationRequest):
    """
    프로젝트와 사용자 정보를 함께 등록
    """
    # 사용자 중복 확인
    if registration.user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    
    # 프로젝트 이름 중복 확인
    for project in projects_db.values():
        if project["name"] == registration.project.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Project name already exists"
            )
    
    try:
        # 사용자 정보 저장
        hashed_password = get_password_hash(registration.user.password)
        user_data = registration.user.dict(exclude={"password"})
        user_data["hashed_password"] = hashed_password
        users_db[registration.user.username] = user_data
        
        # 프로젝트 정보 저장
        project_id = str(uuid.uuid4())
        now = datetime.utcnow()
        project_data = {
            "id": project_id,
            **registration.project.dict(),
            "created_at": now,
            "updated_at": now,
            "owner": user_data
        }
        projects_db[project_id] = project_data
        
        return ProjectResponse(**project_data)
    except Exception as e:
        # 실패 시 저장된 데이터 롤백
        users_db.pop(registration.user.username, None)
        projects_db.pop(project_id, None)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )

@app.get("/projects", response_model=List[ProjectResponse])
async def get_projects(current_user: UserResponse = Depends(get_current_user)):
    """
    등록된 모든 프로젝트 목록 조회
    """
    return [ProjectResponse(**project) for project in projects_db.values()]

@app.post("/streetlights/{streetlight_id}/turn/{command}")
async def control_streetlight(
    streetlight_id: str,
    command: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    가로등 제어 명령 전송
    """
    if command not in ["on", "off"]:
        raise HTTPException(status_code=400, detail="Invalid command")
    
    topic = f"{KAFKA_TOPIC_PREFIX}.{streetlight_id}.turn.{command}"
    message = {
        "command": command,
        "sentAt": datetime.utcnow().isoformat()
    }
    
    producer.send(topic, message)
    return {"status": "success", "message": f"Streetlight {streetlight_id} {command} command sent"}

@app.post("/streetlights/schedule")
async def update_schedule(
    schedule: ScheduleRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    가로등 스케줄 업데이트
    """
    try:
        start_time = datetime.strptime(schedule.startTime, "%H:%M").time()
        end_time = datetime.strptime(schedule.endTime, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format")

    if schedule.season == Season.SUMMER:
        if start_time.hour != 21 or end_time.hour != 6:
            raise HTTPException(
                status_code=400,
                detail="Summer schedule must be from 21:00 to 06:00"
            )
    else:  # WINTER
        if start_time.hour != 19 or end_time.hour != 8:
            raise HTTPException(
                status_code=400,
                detail="Winter schedule must be from 19:00 to 08:00"
            )

    return {"status": "success", "message": f"Schedule updated for {schedule.season}"}

@app.post("/projects/{project_id}/specs", response_model=ApiSpecResponse)
async def create_api_spec(
    project_id: str,
    api_spec: ApiSpecCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    프로젝트에 API 스펙 추가
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # API 스펙 ID 생성
    spec_id = str(uuid.uuid4())
    now = datetime.utcnow()

    try:
        # spec_content를 JSON 형식으로 변환
        spec_content = api_spec.spec_content
        if isinstance(spec_content, str):
            try:
                spec_content = json.loads(spec_content)
            except json.JSONDecodeError:
                spec_content = {"content": spec_content}
        elif not isinstance(spec_content, dict):
            spec_content = {"content": str(spec_content)}

        # MySQL JSON 컬럼을 위한 유효한 JSON 문자열 생성
        json_content = json.dumps(spec_content)
        
        # 데이터 유효성 검증
        try:
            # JSON 파싱 테스트
            json.loads(json_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")

        # API 스펙 데이터 생성
        spec_data = {
            "id": spec_id,
            "project_id": project_id,
            "title": api_spec.title,
            "description": api_spec.description,
            "version": api_spec.version,
            "access_role": api_spec.access_role,
            "spec_content": json_content,  # 유효한 JSON 문자열
            "created_at": now,
            "updated_at": now,
            "created_by": current_user.username,
            "updated_by": current_user.username,
            "is_archived": False
        }
        
        # 데이터베이스에 저장
        api_specs_db[spec_id] = spec_data
        
        return ApiSpecResponse(**spec_data)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create API spec: {str(e)}"
        )

@app.get("/projects/{project_id}/specs", response_model=List[ApiSpecResponse])
async def get_project_specs(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    프로젝트의 API 스펙 목록 조회
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    project_specs = [
        ApiSpecResponse(**spec_data)
        for spec_data in api_specs_db.values()
        if spec_data["project_id"] == project_id
    ]
    
    return project_specs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 