# описание моделей SQLAlckemy (таблицы БД)

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric
from sqlalchemy.sql import func
from core import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="student")  # Student, teacher, admin
    created_at = Column(TIMESTAMP, server_default=func.now())

class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    value = Column(Numeric(4, 2), nullable=False)
    teacher = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    status = Column(String, nullable=False)
    subject = Column(String)
    theme = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
