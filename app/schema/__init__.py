from pydantic import BaseModel

class DiscussionCreate(BaseModel):
    user_id: str
    title: str
    content: str

class DiscussionCreateResponse(BaseModel):
    id: str