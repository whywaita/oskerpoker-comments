from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base, engine_options={'pool_pre_ping': True})


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
    uploaded_at: Mapped[str] = mapped_column(DateTime)
    parsed_text: Mapped[str] = mapped_column(Text)
    fixed_text: Mapped[str] = mapped_column(Text, nullable=True)
