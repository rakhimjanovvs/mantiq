from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal

from app.dependencies import get_course_or_404
from app.schemas import LessonRead, LessonCreate, Page
from app.models import Lesson
from app.database import get_db


router = APIRouter(prefix="/courses", tags=["lessons"])

@router.post("/{course_id}/lessons", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
def create_lesson(course_id: int, lesson_data: LessonCreate, db: Session = Depends(get_db)):
    get_course_or_404(course_id, db)

    existing_lesson = (
        db.query(Lesson)
        .filter(Lesson.course_id == course_id, Lesson.title == lesson_data.title)
        .first()
    )
    
    if existing_lesson:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Урок с таким названием уже существует!"
        )

    new_lesson = Lesson(title=lesson_data.title, content=lesson_data.content, course_id=course_id, video_url=lesson_data.video_url)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson


@router.get("/{course_id}/lessons", response_model=Page[LessonRead])
def list_lessons(
    course_id: int,
    sort: Literal["new", "old"] = "new",
    search: str | None = None,
    limit: int = Query(5, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    get_course_or_404(course_id, db)

    query = db.query(Lesson).filter(Lesson.course_id == course_id)

    if search:
        query = query.filter(Lesson.title.ilike(f"%{search}%"))

    total = query.count()

    if sort == "new":
        query = query.order_by(Lesson.id.desc())
    else:
        query = query.order_by(Lesson.id)

    items = query.offset(offset).limit(limit).all()

    return {"items": items, "total": total, "offset": offset, "limit": limit}