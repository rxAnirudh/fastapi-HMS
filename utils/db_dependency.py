from db.database import SessionLocal
"""
Dependecy
"""
def get_db():
    """Function to get db details"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
