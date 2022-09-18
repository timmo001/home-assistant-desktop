"""Home Assistant Desktop: Models - Database Data"""

from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel


class Data(SQLModel):
    """Database Data"""

    key: str = Field(primary_key=True, nullable=False)
    value: Optional[str] = Field(default=None, nullable=True)
    timestamp: Optional[float] = Field(default=None, nullable=True)


class Secrets(Data, table=True):
    """Database Data Secrets"""


class Settings(Data, table=True):
    """Database Data Settings"""
