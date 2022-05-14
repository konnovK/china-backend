from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from ..config import config


def new_engine(db_user, db_password, db_host, db_name):
    return create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')


engine = new_engine(config.db_user, config.db_password, config.db_host, config.db_name)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
