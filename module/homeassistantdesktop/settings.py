"""Home Assistant Desktop: Settings"""
from __future__ import annotations

import io
import os
from os.path import exists
from typing import Any, Union

from appdirs import AppDirs
from cryptography.fernet import Fernet

from .base import Base
from .common import convert_string_to_correct_type
from .const import (
    SETTING_AUTOSTART,
    SETTING_HOME_ASSISTANT_HOST,
    SETTING_HOME_ASSISTANT_PORT,
    SETTING_HOME_ASSISTANT_SECURE,
    SETTING_HOME_ASSISTANT_SUBSCRIBED_ENTITIES,
    SETTING_LOG_LEVEL,
)
from .database import Database
from .models.database_data import (
    Data as DatabaseData,
    Secrets as DatabaseSecrets,
    Settings as DatabaseSettings,
)


class Settings(Base):
    """Settings"""

    def __init__(
        self,
        database: Database,
    ) -> None:
        """Initialize"""
        super().__init__()
        self._database = database

        # Generate default encryption key
        self._encryption_key: str = ""
        secret_key_path = os.path.join(
            AppDirs("homeassistantdesktop", "timmo001").user_data_dir, "secret.key"
        )
        if exists(secret_key_path):
            with io.open(secret_key_path, encoding="utf-8") as file:
                self._encryption_key = file.read().splitlines()[0]
        if not self._encryption_key:
            self._encryption_key = Fernet.generate_key().decode()
            with io.open(secret_key_path, "w", encoding="utf-8") as file:
                file.write(self._encryption_key)

        # Default Settings
        if self.get(SETTING_AUTOSTART) is None:
            self.set(SETTING_AUTOSTART, str(False))
        if self.get(SETTING_LOG_LEVEL) is None:
            self.set(SETTING_LOG_LEVEL, "INFO")
        if self.get(SETTING_HOME_ASSISTANT_HOST) is None:
            self.set(SETTING_HOME_ASSISTANT_HOST, "homeassistant.local")
        if self.get(SETTING_HOME_ASSISTANT_PORT) is None:
            self.set(SETTING_HOME_ASSISTANT_PORT, "8123")
        if self.get(SETTING_HOME_ASSISTANT_SECURE) is None:
            self.set(SETTING_HOME_ASSISTANT_SECURE, str(False))
        if self.get(SETTING_HOME_ASSISTANT_SUBSCRIBED_ENTITIES) is None:
            self.set(SETTING_HOME_ASSISTANT_SUBSCRIBED_ENTITIES, "[]")

    def get_all(self) -> list[DatabaseData]:
        """Get settings"""
        records = self._database.get_data(DatabaseSettings)
        for record in records:
            if record.value is not None:
                record.value = convert_string_to_correct_type(record.value)
        return records

    def get(
        self,
        key: str,
        default: Union[bool, float, int, str, list[Any], dict[str, Any], None] = None,
    ) -> Union[bool, float, int, str, list[Any], dict[str, Any], None]:
        """Get setting"""
        record = self._database.get_data_item_by_key(DatabaseSettings, key)
        if record is None or record.value is None:
            return None
        result = convert_string_to_correct_type(record.value)
        if result is None:
            return default
        return result

    def get_secret(
        self,
        key: str,
    ) -> str:
        """Get secret"""
        record = self._database.get_data_item_by_key(DatabaseSecrets, key)
        if record is None or record.value is None:
            raise KeyError(f"Secret {key} not found")

        secret = record.value
        fernet = Fernet(self._encryption_key)
        return fernet.decrypt(secret.encode()).decode()

    def set(
        self,
        key: str,
        value: str,
    ) -> None:
        """Set setting"""
        self._database.update_data(
            DatabaseSettings,
            DatabaseSettings(
                key=key,
                value=value,
            ),
        )

    def set_secret(
        self,
        key: str,
        value: str,
    ) -> None:
        """Set secret"""
        fernet = Fernet(self._encryption_key)

        self._database.update_data(
            DatabaseSecrets,
            DatabaseSecrets(
                key=key,
                value=fernet.encrypt(value.encode()).decode(),
            ),
        )
