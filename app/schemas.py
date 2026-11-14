from typing import Annotated, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field, AfterValidator

def clean_title(v: str) -> str:
    v = v.strip()
    if len(v) < 3:
        raise ValueError("Название должно содержать минимум 3 символа")
    return v

def clean_text(v: str) -> str:
    v = v.strip()
    if len(v) < 3:
        raise ValueError("Текст должен содержать минимум 3 символа")
    return v

Title = Annotated[str, Field(min_length=3, max_length=100), AfterValidator(clean_title)]
Content = Annotated[str, Field(min_length=3), AfterValidator(clean_text)]

class CourseCreate(BaseModel):
    title: Title
    description: str = Field(min_length=3, max_length=1000)


class CourseUpdate(CourseCreate):
    pass


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str


class LessonCreate(BaseModel):
    title: Title
    content: Content


class LessonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    course_id: int

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int