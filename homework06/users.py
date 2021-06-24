# import requests
# from bs4 import BeautifulSoup

Base = declarative_base()
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
