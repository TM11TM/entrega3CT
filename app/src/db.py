from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "mariadb+pymysql://fastapi_user:clase123@db:3306/bd_clase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Sesión para hacer consultas en FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base de los modelos
Base = declarative_base()