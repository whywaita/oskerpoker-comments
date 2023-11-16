from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Queue(db.Model):
    __tablename__ = 'queue'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(100), default='pending')


class Movie(db.Model):
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(100))
    parsed_text: Mapped[str] = mapped_column(Text)
    fixed_text: Mapped[str] = mapped_column(Text, nullable=True)
