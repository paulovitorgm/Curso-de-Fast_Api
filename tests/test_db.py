from sqlalchemy import select

from fast_api_curso.models import User


def test_create_user(session):
    user = User(username='paulo_v', email='p@p.com', password='abc123')
    session.add(user)
    session.commit()

    # query
    result = session.scalar(select(User).where(User.email == 'p@p.com'))

    assert result.username == 'paulo_v'
