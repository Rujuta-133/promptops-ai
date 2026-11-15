from sqlalchemy.orm import sessionmaker
from backend.database.config import engine

session_factory = sessionmaker(bind=engine)

def get_db():
    db = session_factory()
    try:
        yield db 
    finally:
        db.close()
