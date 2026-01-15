from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the task")
    description: Optional[str] = Field(None, description="Detailed description of the task")
    user_id: int = Field(..., description="ID of the user creating the task")

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated title of the task")
    description: Optional[str] = Field(None, description="Updated description of the task")
    completed: Optional[bool] = Field(None, description="Updated completion status of the task")

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True