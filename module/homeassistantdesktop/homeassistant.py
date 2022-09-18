"""Home Assistant Desktop: Home Assistant"""

import asyncio

import async_timeout

from .base import Base
from .const import (
    MESSAGE_TYPE_AUTH_INVALID,
    MESSAGE_TYPE_AUTH_OK,
    MESSAGE_TYPE_AUTH_REQUIRED,
    MESSAGE_TYPE_SUCCESS,
    SECRET_HOME_ASSISTANT_TOKEN,
)
from .exceptions import (
    AuthenticationException,
    AuthenticationTokenMissingException,
    ConnectionErrorException,
)
from .models.request import Request
from .models.response import Response
from .settings import Settings
from .websocket_client import WebSocketClient


class HomeAssistant(Base):
    """Home Assistant"""

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        """Initialize"""
        super().__init__()
        self._settings = settings
        self._websocket_client = WebSocketClient(settings)

    @property
    def connected(self) -> bool:
        """Get connection state."""
        return self._websocket_client.connected

    async def _handle_message(
        self,
        response: Response,
    ) -> None:
        """Handle message from Home Assistant"""
        if response.type == MESSAGE_TYPE_AUTH_REQUIRED:
            await self.authenticate()
        elif response.type == MESSAGE_TYPE_SUCCESS:
            self._logger.debug("Received message: %s", response.json())
        else:
            self._logger.warning("Received unknown message: %s", response.json())

    async def authenticate(self) -> None:
        """Authenticate with Home Assistant"""
        token = self._settings.get_secret(SECRET_HOME_ASSISTANT_TOKEN)
        if token is None:
            raise AuthenticationTokenMissingException("No token set")
        response = await self._websocket_client.send_message(
            data={
                "type": "auth",
                "access_token": token,
            },
            wait_for_response=True,
            response_types=[
                MESSAGE_TYPE_AUTH_OK,
                MESSAGE_TYPE_AUTH_INVALID,
            ],
        )
        if response.type == MESSAGE_TYPE_AUTH_OK:
            self._logger.info("Authentication successful: %s", response.ha_version)
        elif response.type == MESSAGE_TYPE_AUTH_INVALID:
            message = "Authentication failed: %s", response.message
            self._logger.error(message)
            raise AuthenticationException(message)

    async def connect(self) -> None:
        """Connect to Home Assistant"""
        try:
            async with async_timeout.timeout(20):
                await self._websocket_client.connect()
        except AuthenticationException as exception:
            self._logger.error("Authentication failed: %s", exception)
        except ConnectionErrorException as exception:
            self._logger.error("Could not connect to WebSocket: %s", exception)
        except asyncio.TimeoutError as exception:
            self._logger.error("Connection timeout to WebSocket: %s", exception)

    async def disconnect(self) -> None:
        """Disconnect from Home Assistant"""
        await self._websocket_client.close()

    async def listen(self) -> None:
        """Listen for messages from Home Assistant"""
        try:
            await self._websocket_client.listen(self._handle_message)
        except AuthenticationException as exception:
            self._logger.error("Authentication failed: %s", exception)
        except ConnectionErrorException as exception:
            self._logger.error("Could not connect to WebSocket: %s", exception)

    # async def get_config(self) -> dict[str, Any]:
    #     """Get Home Assistant config"""
    #     return await self._websocket_client.send_message(Request(data={}))
