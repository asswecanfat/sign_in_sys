from pydantic import BaseModel, Field


class Time(BaseModel):
    seconds: float = Field(..., ge=0, le=60, description="秒")
    minutes: float = Field(..., ge=0, le=60, description="分")
    hours: float = Field(..., ge=0, le=24, description="时")
