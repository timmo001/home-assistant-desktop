"""Home Assistant Desktop: WebSocket Client"""
from __future__ import annotations

import asyncio
from collections.abc import Callable
import json
import socket
from typing import Awaitable, Optional
from uuid import uuid4

import aiohttp

from .base import Base
from .const import (
    MESSAGE_ID,
    MESSAGE_TYPE,
    MESSAGE_TYPE_SUCCESS,
    SETTING_HOME_ASSISTANT_HOST,
    SETTING_HOME_ASSISTANT_PORT,
    SETTING_HOME_ASSISTANT_SECURE,
)
from .exceptions import (
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
        self.current_id = 0
        self._settings = settings
        self._responses: dict[
            str, tuple[asyncio.Future[Response], Optional[list[str]]]
        ] = {}
        self._session: Optional[aiohttp.ClientSession] = None
        self._websocket: Optional[aiohttp.ClientWebSocketResponse] = None

    @property
    def connected(self) -> bool:
        """Get connection state."""
        return self._websocket is not None and not self._websocket.closed

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
        url = f"{'wss' if self._settings.get(SETTING_HOME_ASSISTANT_SECURE) is True else 'ws'}://{self._settings.get(SETTING_HOME_ASSISTANT_HOST)}:{self._settings.get(SETTING_HOME_ASSISTANT_PORT)}/api/websocket"
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

    async def send_message(
        self,
        data: dict,
        wait_for_response: bool = True,
        response_types: Optional[list[str]] = None,
        include_id: bool = True,
    ) -> Response:
        """Send a message to the WebSocket"""
        if not self.connected or self._websocket is None:
            raise ConnectionClosedException("Connection is closed")

        if include_id:
            self.current_id += 1
            data[MESSAGE_ID] = self.current_id

        request = Request(
            id=uuid4().hex,
            data=data,
        )
        future: asyncio.Future[Response] = asyncio.get_running_loop().create_future()
        self._responses[request.id] = future, response_types
        message = json.dumps(request.data)
        await self._websocket.send_str(message)
        self._logger.debug("Sent message: %s", message)
        if wait_for_response:
            try:
                return await future
            finally:
                self._responses.pop(request.id)
        return Response(
            **{
                MESSAGE_ID: request.data[MESSAGE_ID]
                if request.data is not None and request.data[MESSAGE_ID] is not None
                else request.id,
                MESSAGE_TYPE: MESSAGE_TYPE_SUCCESS,
            }  # type: ignore
        )

    async def listen(
        self,
        callback: Optional[Callable[[Response], Awaitable[None]]] = None,
    ) -> None:
        """Listen for messages and map to modules"""

        async def _callback_message(message: dict) -> None:
            """Message Callback"""
            self._logger.debug("New message: %s", message[MESSAGE_TYPE])

            response = Response(**message)

            self._logger.info(
                "Response: %s",
                response.json(
                    include={
                        MESSAGE_ID,
                        MESSAGE_TYPE,
                    },
                    exclude_unset=True,
                ),
            )

            if response.id is not None:
                response_tuple = self._responses.get(response.type)
                if response_tuple is not None:
                    future, response_types = response_tuple
                    if (
                        response_types is not None
                        and response.type not in response_types
                    ):
                        self._logger.info(
                            "Response type '%s' does not match requested types: '%s'.",
                            response.type,
                            response_types,
                        )
                    else:
                        try:
                            future.set_result(response)
                        except asyncio.InvalidStateError:
                            self._logger.warning(
                                "Future already set for response ID: %s",
                                message[MESSAGE_ID],
                            )

            if callback is not None:
                await callback(response)

        await self.listen_for_messages(callback=_callback_message)

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
            raise ConnectionErrorException(self._websocket.exception(), message)

        if message.type in (
            aiohttp.WSMsgType.CLOSE,
            aiohttp.WSMsgType.CLOSED,
            aiohttp.WSMsgType.CLOSING,
        ):
            raise ConnectionClosedException("Connection closed to server", message)

        if message.type == aiohttp.WSMsgType.TEXT:
            message_json = message.json()
            self._logger.debug("Received message: %s", message_json)
            return message_json

        raise BadMessageException(f"Unknown message type: {message.type}", message)
