# type: ignore

from users import Base, User, create_engine, get_session, save_user


def db_set_up(engine):
    Base.metadata.create_all(bind=engine)


def db_tear_down(session):
    session.query(User).delete()
    session.commit()
    session.close()


@pytest.fixture
def engine():
    return create_engine("sqlite://")


@pytest.fixture
def session(engine):
    session = get_session(engine)
    db_set_up(engine)
    yield session
    db_tear_down(session)


def test_user_can_be_saved(session):
    user_id = 1
    user_email = "example@example.com"
    user = User(email=user_email)

    print(f"Email = {user_email}")

    save_user(session, user)

    saved_user = session.query(User).filter(User.id == user_id).first()
    assert saved_user.email == user_email
