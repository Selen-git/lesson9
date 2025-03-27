pip install pytest
pip install sqlalchemy
pip install psycopg2-binary


import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def update_student(name, age):
    student = Student(name=name, age=age)
    session.add(student)
    session.commit()

def update_student(id, name, age):
    student = session.query(Student).get(id)
    student.name = name
    student.age = age
    session.commit()

def delete_student(id):
    student = session.query(Student).get(id)
    session.delete(student)
    session.commit()

def test_add_student():
    add_student('Oleg', 36)
    assert session.query(Student).filter_by(name='Oleg', age=36).count() == 1
  
def test_update_student():
    add_student('Oleg', 36)
    student_id = session.query(Student).filter_by(name='Oleg').first().id
    update_student(student_id, 'Oleg Silkin', 37)
    assert session.query(Student).filter_by(name='Oleg Silkin', age=37).count() == 1
  
def test_delete_student():
    add_student('Oleg Silkin', 37)
    student_id = session.query(Student).filter_by(name='Oleg Silkin').first().id
    delete_student(student_id)
    assert session.query(Student).filter_by(name='Oleg Silkin').count() == 0

def cleanup():
    Student.__table__.drop(engine)

def pytest_sessionfinish(session):
    cleanup()


