"""Home Assistant Desktop: Home Assistant"""

import asyncio
from typing import Any, Optional

import async_timeout

from .base import Base
from .const import (
    MESSAGE_DOMAIN,
    MESSAGE_EVENT_TYPE,
    MESSAGE_SERVICE,
    MESSAGE_SERVICE_DATA,
    MESSAGE_STATE_CHANGED,
    MESSAGE_TYPE,
    MESSAGE_TYPE_AUTH_INVALID,
    MESSAGE_TYPE_AUTH_OK,
    MESSAGE_TYPE_AUTH_REQUIRED,
    MESSAGE_TYPE_CALL_SERVICE,
    MESSAGE_TYPE_EVENT,
    MESSAGE_TYPE_GET_CONFIG,
    MESSAGE_TYPE_GET_SERVICES,
    MESSAGE_TYPE_GET_STATES,
    MESSAGE_TYPE_RESULT,
    MESSAGE_TYPE_SUBSCRIBE_EVENTS,
    MESSAGE_TYPE_SUCCESS,
    SECRET_HOME_ASSISTANT_TOKEN,
)
from .exceptions import (
    AuthenticationException,
    AuthenticationTokenMissingException,
    ConnectionErrorException,
)
from .models.config import Config
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

        self.config: Optional[Config] = None
        self.id_config: Optional[int] = None
        self.id_services: Optional[int] = None
        self.id_states: Optional[int] = None
        self.services: Optional[dict[str, dict[str, Any]]] = None
        self.states: Optional[dict[str, dict]] = None

    @property
    def connected(self) -> bool:
        """Get connection state."""
        return self._websocket_client.connected

    async def _handle_message(
        self,
        response: Response,
    ) -> None:
        """Handle message from Home Assistant"""
        if response.error is not None:
            self._logger.error("Received error: %s", response.error)
        elif response.type == MESSAGE_TYPE_AUTH_REQUIRED:
            await self.authenticate()
        elif response.type == MESSAGE_TYPE_AUTH_OK:
            self._logger.info("Authentication successful: %s", response.ha_version)
            await self.get_config()
            await self.get_services()
            await self.get_states()
            self.id_states = await self.subscribe_events(MESSAGE_STATE_CHANGED)
        elif response.type == MESSAGE_TYPE_AUTH_INVALID:
            self._logger.error("Authentication failed: %s", response.message)
        elif response.type == MESSAGE_TYPE_SUCCESS:
            self._logger.debug("Received message: %s", response.json())
        elif response.type == MESSAGE_TYPE_RESULT:
            self._logger.debug("Received result: %s", response.json())
            if response.id == self.id_config and response.result is not None:
                self.config = Config(**response.result)
                self._logger.info("Set Home Assistant config")
            elif response.id == self.id_services and response.result is not None:
                self.services = response.result
                self._logger.info("Set Home Assistant services")
            elif response.id == self.id_states and response.result is not None:
                self.states = response.result
                self._logger.info("Set Home Assistant states")
        elif response.type == MESSAGE_TYPE_EVENT and response.event is not None:
            self._logger.debug("Received event: %s", response.event)
            if response.event.event_type == MESSAGE_STATE_CHANGED:
                entity_id = response.event.data.get("entity_id")
                state = response.event.data.get("new_state")
                if entity_id is not None and state is not None:
                    if self.states is None:
                        self.states = {}
                    self.states[entity_id] = state
                    self._logger.debug("Updated Home Assistant state: %s", entity_id)
        else:
            self._logger.debug("Received unknown message: %s", response.json())

    async def authenticate(self) -> None:
        """Authenticate with Home Assistant"""
        self._logger.info("Authenticating with Home Assistant")
        token = self._settings.get_secret(SECRET_HOME_ASSISTANT_TOKEN)
        if token is None:
            raise AuthenticationTokenMissingException("No token set")
        # response =
        await self._websocket_client.send_message(
            data={
                "type": "auth",
                "access_token": token,
            },
            wait_for_response=False,
            # response_types=[
            #     MESSAGE_TYPE_AUTH_OK,
            #     MESSAGE_TYPE_AUTH_INVALID,
            # ],
            include_id=False,
        )
        # if response.type == MESSAGE_TYPE_AUTH_OK:
        #     self._logger.info("Authentication successful: %s", response.ha_version)
        # elif response.type == MESSAGE_TYPE_AUTH_INVALID:
        #     message = "Authentication failed: %s", response.message
        #     self._logger.error(message)
        #     raise AuthenticationException(message)

    async def connect(self) -> None:
        """Connect to Home Assistant"""
        self._logger.info("Connecting to Home Assistant")
        try:
            async with async_timeout.timeout(20):
                await self._websocket_client.connect()
        except AuthenticationException as exception:
            self._logger.error("Authentication failed: %s", exception)
        except ConnectionErrorException as exception:
            self._logger.error("Could not connect to WebSocket: %s", exception)
        except asyncio.TimeoutError as exception:
            self._logger.error("Connection timeout to WebSocket: %s", exception)
        self._logger.info("Connected to Home Assistant")

    async def disconnect(self) -> None:
        """Disconnect from Home Assistant"""
        await self._websocket_client.close()

    async def listen(self) -> None:
        """Listen for messages from Home Assistant"""
        self._logger.info("Listen for messages from Home Assistant")
        try:
            await self._websocket_client.listen(self._handle_message)
        except AuthenticationException as exception:
            self._logger.error("Authentication failed: %s", exception)
        except ConnectionErrorException as exception:
            self._logger.error("Could not connect to WebSocket: %s", exception)

        self._logger.info("Stopped listening for messages from Home Assistant")

    async def get_config(self) -> None:
        """Get Home Assistant config"""
        self._logger.info("Getting config from Home Assistant")
        # response =
        await self._websocket_client.send_message(
            data={
                MESSAGE_TYPE: MESSAGE_TYPE_GET_CONFIG,
            },
            wait_for_response=False,
            # wait_for_response=True,
            # response_types=[
            #     MESSAGE_TYPE_RESULT,
            # ],
            include_id=True,
        )
        self.id_config = self._websocket_client.current_id
        # self._logger.info("Received config: %s", response.json())
        # self.config = Config(**response.result)
        # self._logger.info("Set Home Assistant config")

    async def get_services(self) -> None:
        """Get Home Assistant services"""
        self._logger.info("Getting services from Home Assistant")
        # response =
        await self._websocket_client.send_message(
            data={
                MESSAGE_TYPE: MESSAGE_TYPE_GET_SERVICES,
            },
            wait_for_response=False,
            # wait_for_response=True,
            # response_types=[
            #     MESSAGE_TYPE_RESULT,
            # ],
            include_id=True,
        )
        self.id_services = self._websocket_client.current_id
        # self._logger.info("Received services: %s", response.json())
        # self.services = response.result
        # self._logger.info("Set Home Assistant services")

    async def call_service(
        self,
        domain: str,
        service: str,
        service_data: dict[str, Any],
    ) -> None:
        """Call a Home Assistant service"""
        self._logger.info("Calling service %s.%s", domain, service)
        await self._websocket_client.send_message(
            data={
                MESSAGE_TYPE: MESSAGE_TYPE_CALL_SERVICE,
                MESSAGE_DOMAIN: domain,
                MESSAGE_SERVICE: service,
                MESSAGE_SERVICE_DATA: service_data,
            },
            wait_for_response=False,
            # wait_for_response=True,
            # response_types=[
            #     MESSAGE_TYPE_RESULT,
            # ],
            include_id=True,
        )

    async def get_states(self) -> None:
        """Get states of all entities"""
        self._logger.info("Getting states of all entities")
        # response =
        await self._websocket_client.send_message(
            data={
                MESSAGE_TYPE: MESSAGE_TYPE_GET_STATES,
            },
            wait_for_response=False,
            # wait_for_response=True,
            # response_types=[
            #     MESSAGE_TYPE_RESULT,
            # ],
            include_id=True,
        )
        self.id_states = self._websocket_client.current_id
        # self._logger.info("Received states: %s", response.json())
        # self.states = response.result
        # self._logger.info("Set Home Assistant states")

    async def subscribe_events(
        self,
        event_type: str,
    ) -> int:
        """Subscribe to events"""
        self._logger.info("Subscribing to events")
        await self._websocket_client.send_message(
            data={
                MESSAGE_TYPE: MESSAGE_TYPE_SUBSCRIBE_EVENTS,
                MESSAGE_EVENT_TYPE: event_type,
            },
            wait_for_response=False,
            # wait_for_response=True,
            # response_types=[
            #     MESSAGE_TYPE_RESULT,
            # ],
            include_id=True,
        )
        return self._websocket_client.current_id
