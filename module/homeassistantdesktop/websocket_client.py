"""Home Assistant Desktop: WebSocket Client"""
from __future__ import annotations

import asyncio
from collections.abc import Callable
import socket
from typing import Optional
from uuid import uuid4

import aiohttp

from .base import Base
from .const import (
    SETTING_HOME_ASSISTANT_HOST,
    SETTING_HOME_ASSISTANT_PORT,
    SETTING_HOME_ASSISTANT_SECURE,
)
from .exceptions import (
    AuthenticationException,
    BadMessageException,
    ConnectionClosedException,
    ConnectionErrorException,
)
from .models.request import Request
from .models.response import Response
from .settings import Settings


class WebSocketClient(Base):
    """WebSocket Client"""

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        """Initialize"""
        super().__init__()
        self._settings = settings
        self._responses: dict[str, tuple[asyncio.Future[Response], Optional[str]]] = {}
        self._session: Optional[aiohttp.ClientSession] = None
        self._websocket: Optional[aiohttp.ClientWebSocketResponse] = None

    @property
    def connected(self) -> bool:
        """Get connection state."""
        return self._websocket is not None and not self._websocket.closed

    async def _send_message(
        self,
        request: Request,
        wait_for_response: bool = True,
        response_type: Optional[str] = None,
    ) -> Response:
        """Send a message to the WebSocket"""
        if not self.connected or self._websocket is None:
            raise ConnectionClosedException("Connection is closed")

        request.id = uuid4().hex
        future: asyncio.Future[Response] = asyncio.get_running_loop().create_future()
        self._responses[request.id] = future, response_type
        await self._websocket.send_str(request.json())
        self._logger.debug("Sent message: %s", request.json())
        if wait_for_response:
            try:
                return await future
            finally:
                self._responses.pop(request.id)
        return Response(
            id=request.id,
            data={},
        )

    async def close(self) -> None:
        """Close connection"""
        self._logger.info("Closing WebSocket connection")
        if self._websocket is not None:
            await self._websocket.close()
        if self._session is not None:
            await self._session.close()

    async def connect(
        self,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        """Connect to server"""
        if session:
            self._session = session
        else:
            self._session = aiohttp.ClientSession()
        url = f"{self._settings.get(SETTING_HOME_ASSISTANT_SECURE)}://{self._settings.get(SETTING_HOME_ASSISTANT_HOST)}:{self._settings.get(SETTING_HOME_ASSISTANT_PORT)}/api/websocket"
        self._logger.info("Connecting to WebSocket: %s", url)
        try:
            self._websocket = await self._session.ws_connect(url=url, heartbeat=30)
        except (
            aiohttp.WSServerHandshakeError,
            aiohttp.ClientConnectionError,
            socket.gaierror,
        ) as error:
            self._logger.warning(
                "Failed to connect to WebSocket: %s - %s",
                error.__class__.__name__,
                error,
            )
            raise ConnectionErrorException from error
        self._logger.info("Connected to WebSocket")

    async def listen_for_messages(
        self,
        callback: Callable,
    ) -> None:
        """Listen for messages"""
        if not self.connected:
            raise ConnectionClosedException("Connection is closed")

        self._logger.info("Listen for messages")
        if self._websocket is not None:
            while not self._websocket.closed:
                message = await self.receive_message()
                if isinstance(message, dict):
                    await callback(message)

    async def receive_message(self) -> Optional[dict]:
        """Receive message"""
        if not self.connected or self._websocket is None:
            raise ConnectionClosedException("Connection is closed")

        try:
            message = await self._websocket.receive()
        except RuntimeError:
            return None

        if message.type == aiohttp.WSMsgType.ERROR:
            raise ConnectionErrorException(self._websocket.exception())

        if message.type in (
            aiohttp.WSMsgType.CLOSE,
            aiohttp.WSMsgType.CLOSED,
            aiohttp.WSMsgType.CLOSING,
        ):
            raise ConnectionClosedException("Connection closed to server")

        if message.type == aiohttp.WSMsgType.TEXT:
            message_json = message.json()
            self._logger.debug("Received message: %s", message_json)
            return message_json

        raise BadMessageException(f"Unknown message type: {message.type}")
