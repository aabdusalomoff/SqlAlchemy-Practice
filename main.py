from sqlalchemy import create_engine, String, Integer, select, func, update, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from __future__ import annotations

class Base(DeclarativeBase):
    pass


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    experience = Mapped[str] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"Teacher(id={self.id})"
