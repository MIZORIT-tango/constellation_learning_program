from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# (таблица "constellations"), создаю 5 столбцов с атрибутами каждого созвездия
class Constellation(Base):
    __tablename__ = 'constellations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    rus_name = Column(String(100), nullable=False)
    image = Column(LargeBinary, nullable=False)
    hint = Column(String(200), nullable=True)

    # метод для вывойда айди и названия созвездия
    def __repr__(self):
        return f"<Constellation(id={self.id}, name='{self.name}', rus='{self.rus_name}')>"


DATABASE_URL = "postgresql+psycopg2://postgres:mizorit@localhost/star_db"

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()