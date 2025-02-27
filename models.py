from sqlalchemy import Column, Integer, String, ForeignKey, Table
from settings.database import Base
from sqlalchemy.orm import relationship

user_skills = Table(
    'user_skills', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    linkedin_url = Column(String, nullable=True)
    
    education = relationship("Education", back_populates="user", cascade="all, delete-orphan", foreign_keys="[Education.user_id]")
    work_experience = relationship("WorkExperience", back_populates="user", cascade="all, delete-orphan", foreign_keys="[WorkExperience.user_id]")
    skills = relationship("Skill", secondary=user_skills, back_populates="users")

class Education(Base):
    __tablename__ = 'education'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    degree = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="education", foreign_keys=[user_id])

class WorkExperience(Base):
    __tablename__ = 'work_experience'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    key_achievements = Column(String, nullable=True)
    
    user = relationship("User", back_populates="work_experience", foreign_keys=[user_id])

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    
    users = relationship("User", secondary=user_skills, back_populates="skills")

