# generated by datamodel-codegen:
#   filename:  response.json

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Extra, Field


class Response(BaseModel):
    """
    Response
    """

    class Config:
        extra = Extra.allow

    id: Optional[str] = Field(None, description="Message ID")
    type: str = Field(..., description="Type")
    success: Optional[bool] = Field(None, description="Success")
    message: Optional[str] = Field(None, description="Message")
    event_type: Optional[str] = Field(None, description="Event Type")
    result: Optional[Any] = Field(None, description="Result")
    ha_version: Optional[str] = Field(None, description="Home Assistant Version")
