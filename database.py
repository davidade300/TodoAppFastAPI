from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sqlite:///./todos.db -> can be used too, but root folder will be the vsc ws folder
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:220498@localhost/TodoApplicationDatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
