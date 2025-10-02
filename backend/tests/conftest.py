import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.interface import app
from app.infrastructure.database import get_db
from app.domain.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    
    with TestClient(app) as test_client:
        yield test_client
    
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_user_data():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "11999999999",
        "user_type": "general"
    }

@pytest.fixture
def sample_post_data():
    return {
        "title": "Test Post",
        "content": "This is a test post content",
        "category": "general",
        "author_id": 1
    }

@pytest.fixture
def sample_comment_data():
    return {
        "content": "This is a test comment",
        "post_id": 1,
        "author_id": 1
    }
