"""Home Assistant Desktop: Database"""
from __future__ import annotations

from collections.abc import Mapping
import os
from time import time
from typing import Any, Optional, Union

from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.sql.expression import Select, SelectOfScalar

from .base import Base
from .common import get_user_data_directory
from .const import MODEL_SECRETS, MODEL_SETTINGS
from .models.database_data import Secrets, Settings, SubscribedEntities

TABLE_MAP: Mapping[str, Any] = {
    MODEL_SECRETS: Secrets,
    MODEL_SETTINGS: Settings,
}


TableDataType = Union[
    Secrets,
    Settings,
]


SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


class Database(Base):
    """Database"""

    def __init__(self):
        """Initialise"""
        super().__init__()
        self._engine = create_engine(
            f"sqlite:///{os.path.join(get_user_data_directory(), 'homeassistantdesktop.db')}"
        )
        SQLModel.metadata.create_all(
            self._engine,
            # tables=TABLES,
        )

    def clear_table(
        self,
        table: Any,
    ) -> None:
        """Clear table"""
        with Session(self._engine, autoflush=True) as session:
            for sensor in session.exec(select(table)).all():
                session.delete(sensor)
            session.commit()

    def get_data(
        self,
        table: Any,
    ) -> list[Any]:
        """Get data from database"""
        with Session(self._engine, autoflush=True) as session:
            return session.exec(select(table)).all()

    def get_data_by_key(
        self,
        table: Any,
        key: str,
    ) -> list[Any]:
        """Get data from database by key"""
        with Session(self._engine, autoflush=True) as session:
            return session.exec(select(table).where(table.key == key)).all()

    def get_data_item_by_key(
        self,
        table: Any,
        key: str,
    ) -> Optional[Any]:
        """Get data item from database by key"""
        with Session(self._engine, autoflush=True) as session:
            return session.exec(select(table).where(table.key == key)).first()

    def update_data(
        self,
        table,
        data: Any,
    ) -> None:
        """Update data"""
        with Session(self._engine, autoflush=True) as session:
            result = session.exec(select(table).where(table.key == data.key))
            if (old_data := result.first()) is None:
                data.timestamp = time()
                session.add(data)
            else:
                old_data.value = data.value
                old_data.timestamp = time()
                session.add(old_data)
            session.commit()
            if old_data is not None:
                session.refresh(old_data)

    def update_subscribed_entities(
        self,
        entities: list[str],
    ) -> None:
        """Update data"""
        self.clear_table(SubscribedEntities)
        with Session(self._engine, autoflush=True) as session:
            for entity in entities:
                session.add(SubscribedEntities(entity_id=entity, timestamp=time()))
            session.commit()
