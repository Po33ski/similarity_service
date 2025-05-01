from sqlalchemy.engine import URL
from sqlalchemy import create_engine

def get_db_url():
    return URL.create(
        drivername="postgresql+psycopg",
        username="postgres",
        password="password",
        host="localhost",
        port=5556,  # Your Docker Compose port
        database="similarity_search_service_db"
    )

def get_engine():
    return create_engine(get_db_url())