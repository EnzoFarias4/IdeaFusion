from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

db_user = os.getenv('DATABASE_USER')
db_password = os.getenv('DATABASE_PASSWORD')
db_host = os.getenv('DATABASE_HOST')
db_port = os.getenv('DATABASE_PORT', '5432')
db_name = os.getenv('DATABASE_NAME')
db_connection_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

database_engine = create_engine(db_connection_url)
DatabaseSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=database_engine))

def get_database_session():
    db_session = DatabaseSession()
    try:
        yield db_session
    finally:
        db_session.close()

@lru_cache(maxsize=32)
def get_records_with_cache(first_param, second_param):
    db_session = next(get_database_session())
    query_result = db_session.execute(
        "SELECT * FROM some_table WHERE column1 = :first_param AND column2 = :second_param",
        {"first_param": first_param, "second_param": second_param}
    ).fetchall()
    return query_result