from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
# from dotenv import load_dotenv
import pdb

# 환경 변수 로드
# load_dotenv()

# 데이터베이스 URL 설정
# 환경 변수에서 데이터베이스 URL을 가져오거나 기본값 사용
# 오류: pymysql 모듈이 설치되어 있지 않음
# mysql+pymysql 대신 mysql 사용 또는 pymysql 설치 필요
# SQLALCHEMY_DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "mysql+pymysql://testuser:1234@localhost:3306/mydb"  # mysql+pymysql:// -> mysql://로 변경
# )


# 데이터베이스 엔진 설정
# SQLite 사용 시 check_same_thread=False 설정 필요
engine = create_engine(
   "mysql+pymysql://testuser:1234@localhost:3306/mydb",
    # SQLite 사용 시에만 connect_args 추가
    connect_args={}, # {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {},
    # 에코 모드 설정 (SQL 쿼리 로깅)
    echo=bool(os.getenv("SQL_ECHO", "False").lower() == "true"),
    # 커넥션 풀 설정
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    pool_timeout=float(os.getenv("DB_POOL_TIMEOUT", "30")),
    pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "1800")),
)

# 세션 팩토리 생성
# autocommit=False: 명시적인 커밋 필요
# autoflush=False: 명시적인 플러시 필요
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 모델 기본 클래스 생성
Base = declarative_base()

def get_db() -> Generator:
    """
    데이터베이스 세션을 생성하고 관리하는 의존성 주입 함수
    
    Yields:
        Session: 데이터베이스 세션 객체
        
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    pdb.set_trace()
    print("------------------- session Mamer", db, sessionmaker)
    pdb.set_trace()
    try:
        yield db
    finally:
        db.close()

class DatabaseSessionManager:
    """
    데이터베이스 세션 관리를 위한 컨텍스트 매니저 클래스
    
    Example:
        with DatabaseSessionManager() as db:
            user = db.query(User).first()
            db.commit()
    """
    
    def __init__(self):
        # pdb.set_trace()
        self.db = SessionLocal()
        
    def __enter__(self):
        return self.db
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

def init_db() -> None:
    """
    데이터베이스 초기화 함수
    모든 테이블을 생성합니다.
    
    Example:
        if __name__ == "__main__":
            init_db()
    """
    try:
        # 모든 모델의 테이블 생성
        Base.metadata.create_all(bind=engine)
        print("Successfully initialized database.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise

def close_db() -> None:
    """
    데이터베이스 연결을 종료하는 함수
    애플리케이션 종료 시 호출됩니다.
    """
    try:
        engine.dispose()
        print("Successfully closed database connections.")
    except Exception as e:
        print(f"Failed to close database connections: {e}")
        raise

# 환경 변수 설정 예시를 위한 주석
"""
데이터베이스 설정을 위한 환경 변수 예시 (.env 파일):

# 데이터베이스 연결 설정
DATABASE_URL=postgresql://user:password@localhost:5432/api_hub
# DATABASE_URL=mysql://user:password@localhost:3306/api_hub
# DATABASE_URL=sqlite:///./api-hub.db

# SQL 쿼리 로깅 설정
SQL_ECHO=False

# 데이터베이스 풀 설정
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
"""

# 사용 예시를 위한 주석
"""
# FastAPI에서 데이터베이스 세션 사용 예시:

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 컨텍스트 매니저를 사용한 데이터베이스 세션 관리 예시:

def create_user(user_data: dict):
    with DatabaseSessionManager() as db:
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
"""
