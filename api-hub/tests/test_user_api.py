import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..api_hub.db.database import Base, get_db
from ..api_hub.main import app
from ..api_hub.models.user import User

# 테스트용 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """테스트용 데이터베이스 세션 제공"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 테스트용 데이터베이스 의존성 주입
app.dependency_overrides[get_db] = override_get_db

# 테스트 클라이언트 생성
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """
    각 테스트 실행 전에 테스트 데이터베이스를 초기화하는 fixture
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    """사용자 생성 테스트"""
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data

def test_create_user_duplicate_email():
    """중복된 이메일로 사용자 생성 시도 테스트"""
    # 첫 번째 사용자 생성
    client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser1",
            "password": "testpass123"
        }
    )
    
    # 동일한 이메일로 두 번째 사용자 생성 시도
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser2",
            "password": "testpass123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_read_user():
    """사용자 조회 테스트"""
    # 사용자 생성
    create_response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    user_id = create_response.json()["id"]
    
    # 생성된 사용자 조회
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_read_user_not_found():
    """존재하지 않는 사용자 조회 테스트"""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_user():
    """사용자 정보 업데이트 테스트"""
    # 사용자 생성
    create_response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    user_id = create_response.json()["id"]
    
    # 사용자 정보 업데이트
    response = client.put(
        f"/users/{user_id}",
        json={
            "username": "updated_user",
            "email": "updated@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updated_user"
    assert data["email"] == "updated@example.com"

def test_delete_user():
    """사용자 삭제 테스트"""
    # 사용자 생성
    create_response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    user_id = create_response.json()["id"]
    
    # 사용자 삭제
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    # 삭제된 사용자 조회 시도
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404 