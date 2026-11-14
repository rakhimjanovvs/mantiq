from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal

from app.schemas import CourseCreate, CourseRead, CourseUpdate, Page
from app.models import Course
from app.database import get_db
from app.dependencies import get_course_or_404

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    existing_course = (
        db.query(Course).filter_by(title=course_data.title).first()
    )

    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Курс с таким названием уже существует!"
        )

    new_course = Course(title=course_data.title, description=course_data.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

    
@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, course_data: CourseUpdate, db: Session=Depends(get_db)):
    course = get_course_or_404(course_id, db)

    conflict = (
        db.query(Course)
        .filter(Course.title == course_data.title, Course.id != course_id)
        .first()
    )

    if conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Курс с таким названием уже существует!"
        )

    course.title = course_data.title
    course.description = course_data.description

    db.commit()
    db.refresh(course)

    return course


@router.get("/", response_model=Page[CourseRead])
def list_courses(
    sort: Literal["new", "old"] = "new",
    search: str | None = None,
    limit: int = Query(5, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    
    query = db.query(Course)

    if search:
        query = query.filter(Course.title.ilike(f"%{search}%"))

    total = query.count()

    if sort == "new":
        query = query.order_by(Course.id.desc())
    else:
        query = query.order_by(Course.id)

    items = query.offset(offset).limit(limit).all()

    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = get_course_or_404(course_id, db)
    db.delete(course)
    db.commit()