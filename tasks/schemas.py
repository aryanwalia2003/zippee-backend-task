from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class TaskUpdateSchema(BaseModel):
    task_id: int
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    
    @field_validator('title', 'description')
    @classmethod
    def check_at_least_one(cls, v, values):
        return v

class TaskCompleteSchema(BaseModel):
    task_id: int
    completed: bool
