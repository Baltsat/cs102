# type: ignore

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # type: ignore

SQLALCHEMY_DATABASE_URL = "sqlite:///users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)


def get_session(engine) -> Session:
    SessionLocal.configure(bind=engine)
    return SessionLocal()


def save_user(session: Session, user: User) -> None:
    session.add(user)
    session.commit()
