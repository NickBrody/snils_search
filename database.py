from typing import Dict, Any

from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://admin:123@localhost:5432/documents")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Document(Base):
    __tablename__ = 'snils_data'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    snils = Column(String, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}
