from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Course

def get_course_or_404(course_id: int, db: Session) -> Course:
     course = db.get(Course, course_id)
     if not course:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Курс не найден!")
     return course