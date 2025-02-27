from pydantic import BaseModel
from typing import List , Optional
from models import User

# Pydantic models for request validation
class EducationCreate(BaseModel):
    degree: str
    institution: str
    year: int

class WorkExperienceCreate(BaseModel):
    company: str
    role: str
    duration: str
    key_achievements: Optional[str]

class SkillCreate(BaseModel):
    name: str

class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    linkedin_url: Optional[str]
    education: List[EducationCreate]
    work_experience: List[WorkExperienceCreate]
    skills: List[str]

class EducationUpdate(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[int] = None

class WorkExperienceUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    key_achievements: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    education: Optional[List[EducationUpdate]] = None
    work_experience: Optional[List[WorkExperienceUpdate]] = None
    skills: Optional[List[str]] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    linkedin_url: Optional[str]
    education: List[EducationCreate]
    work_experience: List[WorkExperienceCreate]
    skills: List[str]

    class Config:
        from_attributes = True  # ✅ Use this in Pydantic v2

    @staticmethod
    def from_user(user: User):
        """Converts a User SQLAlchemy object into a UserResponse Pydantic model."""
        return UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            linkedin_url=user.linkedin_url,
            education=[EducationCreate(**edu.__dict__) for edu in user.education],
            work_experience=[WorkExperienceCreate(**exp.__dict__) for exp in user.work_experience],
            skills=[skill.name for skill in user.skills]
        )

