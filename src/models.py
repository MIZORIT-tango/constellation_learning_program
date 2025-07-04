from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base
from database import engine

Base = declarative_base()

# Определение модели Constellation
class Constellation(Base):
    __tablename__ = 'constellations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    rus_name = Column(String(100), nullable=False)
    image = Column(LargeBinary, nullable=False)
    hint = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<Constellation(id={self.id}, name='{self.name}', rus='{self.rus_name}')>"


Base.metadata.create_all(engine)