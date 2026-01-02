from pydantic import BaseModel, Field


class IdSchema(BaseModel):
    id: int = Field(examples=[123], gt=0)
