from typing import Dict, Any

from sqlalchemy import Column, Integer,create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://admin:admin@db:5432/test_db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    number = Column(Integer, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}
