import sqlalchemy as sql
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db/db.db')
Base = declarative_base(bind=engine)
session = sessionmaker(bind=engine)()


class SaveDeleteModelMixin:
    def save(self):
        try:
            session.add(self)
            session.commit()
        except:
            session.rollback()
            raise
        return self

    def delete(self):
        session.delete(self)
        session.commit()


class Bot(Base, SaveDeleteModelMixin):
    __tablename__ = "bot_records"

    pid = sql.Column(sql.Integer, primary_key=True)
    start = sql.Column(sql.DATETIME)
    end = sql.Column(sql.DATETIME, nullable=True)

    def serialize(self):
        return {"pid": self.pid,
                "start": self.start,
                "end": self.end if self.end is not None else "still alive"}


if not Bot.__tablename__ in Base.metadata.tables:
    Base.metadata.create_all()
