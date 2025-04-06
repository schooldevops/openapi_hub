import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app, Season, UserRole, AccessRole

client = TestClient(app)

def test_project_registration():
    """
    프로젝트 등록 테스트
    """
    response = client.post(
        "/projects",
        json={
            "project": {
                "name": "Test Project",
                "description": "A test project",
                "location": "Test Location"
            },
            "user": {
                "username": "testuser",
                "password": "testpass",
                "email": "test@example.com",
                "full_name": "Test User",
                "role": "ADMIN"
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["location"] == "Test Location"
    assert data["owner"]["username"] == "testuser"
    assert data["owner"]["role"] == "ADMIN"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_login_with_json():
    """
    JSON 형식으로 로그인 테스트
    """
    # 먼저 사용자 등록
    client.post(
        "/projects",
        json={
            "project": {
                "name": "JSON Login Test Project",
                "description": "A project for testing JSON login",
                "location": "Test Location"
            },
            "user": {
                "username": "jsonuser",
                "password": "testpass",
                "email": "json@example.com",
                "full_name": "JSON User",
                "role": "ADMIN"
            }
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "jsonuser",
            "password": "testpass"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_with_form():
    """
    Form 데이터로 로그인 테스트
    """
    # 먼저 사용자 등록
    client.post(
        "/projects",
        json={
            "project": {
                "name": "Form Login Test Project",
                "description": "A project for testing form login",
                "location": "Test Location"
            },
            "user": {
                "username": "formuser",
                "password": "testpass",
                "email": "form@example.com",
                "full_name": "Form User",
                "role": "ADMIN"
            }
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "formuser",
            "password": "testpass",
            "grant_type": "password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_duplicate_project_registration():
    """
    중복 프로젝트 등록 테스트
    """
    # 첫 번째 프로젝트 등록
    response = client.post(
        "/projects",
        json={
            "project": {
                "name": "Duplicate Project",
                "description": "A duplicate project",
                "location": "Test Location"
            },
            "user": {
                "username": "dupuser",
                "password": "testpass",
                "email": "dup@example.com",
                "full_name": "Duplicate User",
                "role": "ADMIN"
            }
        }
    )
    assert response.status_code == 201

    # 동일한 프로젝트 이름으로 다시 등록
    response = client.post(
        "/projects",
        json={
            "project": {
                "name": "Duplicate Project",
                "description": "Another duplicate project",
                "location": "Another Location"
            },
            "user": {
                "username": "dupuser2",
                "password": "testpass",
                "email": "dup2@example.com",
                "full_name": "Duplicate User 2",
                "role": "ADMIN"
            }
        }
    )
    assert response.status_code == 409

def test_get_projects():
    """
    프로젝트 목록 조회 테스트
    """
    # 먼저 사용자 등록 및 로그인
    client.post(
        "/projects",
        json={
            "project": {
                "name": "List Test Project",
                "description": "A project for testing list",
                "location": "Test Location"
            },
            "user": {
                "username": "listuser",
                "password": "testpass",
                "email": "list@example.com",
                "full_name": "List User",
                "role": "ADMIN"
            }
        }
    )

    # 로그인하여 토큰 획득
    login_response = client.post(
        "/auth/login",
        json={
            "username": "listuser",
            "password": "testpass"
        }
    )
    token = login_response.json()["access_token"]
    
    # 프로젝트 목록 조회
    response = client.get(
        "/projects",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) > 0
    assert any(p["name"] == "List Test Project" for p in projects)

def test_control_streetlight_unauthorized():
    """
    인증되지 않은 가로등 제어 요청 테스트
    """
    response = client.post("/streetlights/1/turn/on")
    assert response.status_code == 401

def test_control_streetlight_authorized():
    """
    인증된 가로등 제어 요청 테스트
    """
    # 먼저 사용자 등록
    client.post(
        "/projects",
        json={
            "project": {
                "name": "Control Test Project",
                "description": "A project for testing control",
                "location": "Test Location"
            },
            "user": {
                "username": "controluser",
                "password": "testpass",
                "email": "control@example.com",
                "full_name": "Control User",
                "role": "OPERATOR"
            }
        }
    )

    # 로그인하여 토큰 획득
    login_response = client.post(
        "/auth/login",
        json={
            "username": "controluser",
            "password": "testpass"
        }
    )
    token = login_response.json()["access_token"]
    
    # 토큰을 사용하여 가로등 제어 요청
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/streetlights/1/turn/on",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_invalid_schedule():
    """
    잘못된 스케줄 설정 테스트
    """
    # 먼저 사용자 등록 및 로그인
    client.post(
        "/projects",
        json={
            "project": {
                "name": "Schedule Test Project",
                "description": "A project for testing schedule",
                "location": "Test Location"
            },
            "user": {
                "username": "scheduleuser",
                "password": "testpass",
                "email": "schedule@example.com",
                "full_name": "Schedule User",
                "role": "ADMIN"
            }
        }
    )

    # 로그인
    login_response = client.post(
        "/auth/login",
        json={
            "username": "scheduleuser",
            "password": "testpass"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 잘못된 시간 형식으로 요청
    response = client.post(
        "/streetlights/schedule",
        headers=headers,
        json={
            "season": "SUMMER",
            "startTime": "invalid",
            "endTime": "invalid"
        }
    )
    assert response.status_code == 400

def test_valid_summer_schedule():
    """
    올바른 하절기 스케줄 설정 테스트
    """
    # 로그인
    login_response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 올바른 하절기 시간 설정
    response = client.post(
        "/streetlights/schedule",
        headers=headers,
        json={
            "season": "SUMMER",
            "startTime": "21:00",
            "endTime": "06:00"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_valid_winter_schedule():
    """
    올바른 동절기 스케줄 설정 테스트
    """
    # 로그인
    login_response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 올바른 동절기 시간 설정
    response = client.post(
        "/streetlights/schedule",
        headers=headers,
        json={
            "season": "WINTER",
            "startTime": "19:00",
            "endTime": "08:00"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_create_api_spec():
    """
    API 스펙 생성 테스트
    """
    # 프로젝트와 사용자 등록
    project_response = client.post(
        "/projects",
        json={
            "project": {
                "name": "API Spec Test Project",
                "description": "A project for testing API specs",
                "location": "Test Location"
            },
            "user": {
                "username": "specuser",
                "password": "testpass",
                "email": "spec@example.com",
                "full_name": "Spec User",
                "role": "ADMIN"
            }
        }
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # 로그인
    login_response = client.post(
        "/auth/login",
        json={
            "username": "specuser",
            "password": "testpass"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # API 스펙 생성
    spec_data = {
        "title": "Test API",
        "description": "Test API Description",
        "version": "1.0.0",
        "spec_content": {
            "openapi": "3.0.0",
            "info": {
                "title": "Test API",
                "version": "1.0.0"
            },
            "paths": {}
        },
        "access_role": "private",
        "project_id": project_id
    }

    response = client.post(
        f"/projects/{project_id}/specs",
        headers=headers,
        json=spec_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test API"
    assert data["version"] == "1.0.0"
    assert data["project_id"] == project_id
    assert not data["is_archived"]

def test_create_api_spec_invalid_json():
    """
    잘못된 JSON으로 API 스펙 생성 시도 테스트
    """
    # 프로젝트와 사용자 등록
    project_response = client.post(
        "/projects",
        json={
            "project": {
                "name": "Invalid JSON Test Project",
                "description": "A project for testing invalid JSON",
                "location": "Test Location"
            },
            "user": {
                "username": "invalidjsonuser",
                "password": "testpass",
                "email": "invalid@example.com",
                "full_name": "Invalid JSON User",
                "role": "ADMIN"
            }
        }
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # 로그인
    login_response = client.post(
        "/auth/login",
        json={
            "username": "invalidjsonuser",
            "password": "testpass"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 잘못된 JSON으로 API 스펙 생성 시도
    spec_data = {
        "title": "Invalid API",
        "description": "Invalid API Description",
        "version": "1.0.0",
        "spec_content": "Invalid JSON",
        "access_role": "private",
        "project_id": project_id
    }

    response = client.post(
        f"/projects/{project_id}/specs",
        headers=headers,
        json=spec_data
    )
    assert response.status_code == 400

def test_get_project_specs():
    """
    프로젝트의 API 스펙 목록 조회 테스트
    """
    # 프로젝트와 사용자 등록
    project_response = client.post(
        "/projects",
        json={
            "project": {
                "name": "Spec List Test Project",
                "description": "A project for testing spec list",
                "location": "Test Location"
            },
            "user": {
                "username": "speclistuser",
                "password": "testpass",
                "email": "speclist@example.com",
                "full_name": "Spec List User",
                "role": "ADMIN"
            }
        }
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # 로그인
    login_response = client.post(
        "/auth/login",
        json={
            "username": "speclistuser",
            "password": "testpass"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # API 스펙 생성
    spec_data = {
        "title": "List Test API",
        "description": "List Test API Description",
        "version": "1.0.0",
        "spec_content": {
            "openapi": "3.0.0",
            "info": {
                "title": "List Test API",
                "version": "1.0.0"
            },
            "paths": {}
        },
        "access_role": "private",
        "project_id": project_id
    }

    # API 스펙 생성
    create_response = client.post(
        f"/projects/{project_id}/specs",
        headers=headers,
        json=spec_data
    )
    assert create_response.status_code == 200

    # API 스펙 목록 조회
    list_response = client.get(
        f"/projects/{project_id}/specs",
        headers=headers
    )
    assert list_response.status_code == 200
    specs = list_response.json()
    assert len(specs) > 0
    assert specs[0]["title"] == "List Test API"
    assert specs[0]["project_id"] == project_id 