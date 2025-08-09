from __future__ import annotations

import os
from sqlalchemy.engine import URL
from sqlalchemy import create_engine


def get_db_url() -> URL:
    return URL.create(
        drivername=os.getenv("DB_DRIVER", "postgresql+psycopg"),
        username=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5556")),
        database=os.getenv("DB_NAME", "similarity_search_service_db"),
    )


def get_engine():
    return create_engine(get_db_url())


