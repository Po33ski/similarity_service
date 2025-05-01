from database import get_engine
from models import Base

def initialize_database():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    initialize_database()
