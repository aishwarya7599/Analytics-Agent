from sqlmodel import SQLModel, create_engine, Session
from .config import DB_URL

engine = create_engine(DB_URL, echo=False)

def init_db() -> None:
    from . import models  # noqa: F401  (register tables)
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
