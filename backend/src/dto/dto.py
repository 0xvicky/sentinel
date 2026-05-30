from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    query: str = Field(alias="query")
    session_id: str = Field(alias="sessionId")

    class Config:
        populate_by_name = True
        extra = "forbid"
