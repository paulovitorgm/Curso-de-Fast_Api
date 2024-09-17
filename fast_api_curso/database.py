from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_api_curso.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

# o comentário 'pragma: no cover' quer dizer
# que o código não será coberto por testes


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
