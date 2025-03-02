-- 사용자 테이블
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY comment '사용자 아이디',
    email VARCHAR(255) UNIQUE NOT NULL comment '사용자 이메일',
    password_hash VARCHAR(255) NOT NULL comment '사용자 비밀번호',
    full_name VARCHAR(100) NOT NULL comment '사용자 이름',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL comment '사용자 생성일',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP comment '사용자 수정일'
) comment '사용자 테이블';

-- 프로젝트 테이블
DROP TABLE IF EXISTS projects;
CREATE TABLE projects (
    id BIGINT AUTO_INCREMENT PRIMARY KEY comment '프로젝트 아이디',
    name VARCHAR(100) NOT NULL comment '프로젝트 이름',
    description VARCHAR(500) comment '프로젝트 설명',
    is_archived BOOLEAN DEFAULT FALSE comment '프로젝트 삭제 여부',
    created_by BIGINT comment '프로젝트 생성자 아이디',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL comment '프로젝트 생성일',
    updated_by BIGINT comment '프로젝트 수정자 아이디' ,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP comment '프로젝트 수정일'
) comment '프로젝트 테이블';

-- 프로젝트 멤버 테이블
DROP TABLE IF EXISTS project_members;
CREATE TABLE project_members (
    id BIGINT AUTO_INCREMENT PRIMARY KEY comment '프로젝트 멤버 아이디',
    project_id BIGINT comment '프로젝트 아이디',
    user_id BIGINT comment '사용자 아이디',
    member_role VARCHAR(20) NOT NULL comment '프로젝트 멤버 역할',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL comment '프로젝트 멤버 생성일',
    UNIQUE(project_id, user_id)
) comment '프로젝트 멤버 테이블';

-- API 문서 테이블
DROP TABLE IF EXISTS api_specs;
CREATE TABLE api_specs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY comment 'API 문서 아이디',
    project_id BIGINT comment '프로젝트 아이디',
    version VARCHAR(20) NOT NULL comment 'API 문서 버전',
    title VARCHAR(255) NOT NULL comment 'API 문서 제목',
    description TEXT comment 'API 문서 설명',
    spec_content JSON comment 'API 문서 내용',
    is_archived BOOLEAN DEFAULT FALSE comment 'API 문서 삭제 여부',
    access_role VARCHAR(20) NOT NULL comment 'API 문서 접근 역할',
    created_by BIGINT comment 'API 문서 생성자 아이디',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL comment 'API 문서 생성일',
    updated_by BIGINT comment '프로젝트 수정자 아이디' ,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP comment 'API 문서 수정일',
    UNIQUE(project_id, version)
) comment 'API 문서 테이블';

-- 프로젝트 Credential 테이블
DROP TABLE IF EXISTS project_credentials;
CREATE TABLE project_credentials (
    id BIGINT AUTO_INCREMENT PRIMARY KEY comment '프로젝트 Credential 아이디',
    project_id BIGINT comment '프로젝트 아이디',
    api_key VARCHAR(255) NOT NULL comment 'API 키',
    api_secret VARCHAR(255) NOT NULL comment 'API 시크릿',
    created_by BIGINT comment 'API 문서 생성자 아이디',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL comment '프로젝트 Credential 생성일',
    expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL comment '프로젝트 Credential 만료일 기본 90일'
) comment '프로젝트 Credential 테이블';

-- Foreign Key 관계
ALTER TABLE projects ADD FOREIGN KEY (created_by) REFERENCES users(id);
ALTER TABLE projects ADD FOREIGN KEY (updated_by) REFERENCES users(id);
ALTER TABLE project_members ADD FOREIGN KEY (project_id) REFERENCES projects(id);
ALTER TABLE project_members ADD FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE api_specs ADD FOREIGN KEY (project_id) REFERENCES projects(id);
ALTER TABLE api_specs ADD FOREIGN KEY (created_by) REFERENCES users(id);
ALTER TABLE api_specs ADD FOREIGN KEY (updated_by) REFERENCES users(id);
ALTER TABLE project_credentials ADD FOREIGN KEY (project_id) REFERENCES projects(id);
ALTER TABLE project_credentials ADD FOREIGN KEY (created_by) REFERENCES users(id);