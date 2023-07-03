from pydantic import BaseModel, Field

class DiscussionCreate(BaseModel):
    title: str
    content: str

class Discussion(DiscussionCreate):
    user_id: str

class DiscussionCreateResponse(BaseModel):
    id: str

class DiscussionSearchResponse(BaseModel):
    id: str = Field(..., alias="_id")
    score: float = Field(..., alias="_score")
    source: Discussion = Field(..., alias="_source")