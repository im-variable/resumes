from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, UserUpdate
from settings.database import get_db
from models import User, Education, WorkExperience, Skill
from typing import List
from starlette import status
router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_resume(resume_data: UserCreate, db: Session = Depends(get_db)):
    user = User(
        full_name=resume_data.full_name,
        email=resume_data.email,
        phone=resume_data.phone,
        linkedin_url=resume_data.linkedin_url
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    for edu in resume_data.education:
        education = Education(user_id=user.id, degree=edu.degree, institution=edu.institution, year=edu.year)
        db.add(education)

    for exp in resume_data.work_experience:
        work_experience = WorkExperience(user_id=user.id, company=exp.company, role=exp.role, duration=exp.duration, key_achievements=exp.key_achievements)
        db.add(work_experience)


    for skill_name in resume_data.skills:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.add(skill)
        user.skills.append(skill)
    
    db.commit()
    
    return user

@router.get("/", response_model=List[UserResponse])
async def resume_list(db: Session = Depends(get_db), page:int=1, limit:int=5):
    users = db.query(User).offset((page - 1) * limit).limit(limit).all()
    return [UserResponse.from_user(user) for user in users]

@router.get("/{id}", response_model=UserResponse)
async def get_resume(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Resume not found")
    return UserResponse.from_user(user)

@router.put("/{id}", response_model=UserResponse)
async def update_resume(id: int, resume_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Update user fields
    user.full_name = resume_data.full_name or user.full_name
    user.phone = resume_data.phone or user.phone
    user.linkedin_url = resume_data.linkedin_url or user.linkedin_url

    # Update education data
    if resume_data.education:
        db.query(Education).filter(Education.user_id == id).delete()
        for edu in resume_data.education:
            education = Education(user_id=user.id, degree=edu.degree, institution=edu.institution, year=edu.year)
            db.add(education)

    # Update experience data
    if resume_data.work_experience:
        db.query(WorkExperience).filter(WorkExperience.user_id == id).delete()
        for exp in resume_data.work_experience:
            work_experience = WorkExperience(user_id=user.id, company=exp.company, role=exp.role, duration=exp.duration, key_achievements=exp.key_achievements)
            db.add(work_experience)

    # Update skills data
    if resume_data.skills:
        user.skills.clear()
        for skill_name in resume_data.skills:
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.add(skill)
            user.skills.append(skill)

    db.commit()
    return UserResponse.from_user(user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(user)
    db.commit()
    return {"message": "Resume deleted successfully"}
