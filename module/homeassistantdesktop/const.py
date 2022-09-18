"""Home Assistant Desktop: Constants"""


# Logging
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FORMAT = "%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s"

# Database
TABLE_SECRETS = "secrets"
TABLE_SETTINGS = "settings"

COLUMN_KEY = "key"
COLUMN_NAME = "name"
COLUMN_TIMESTAMP = "timestamp"
COLUMN_TYPE = "type"
COLUMN_VALUE = "value"

# Message
MESSAGE_ACCESS_TOKEN = "access_token"
MESSAGE_DOMAIN = "domain"
MESSAGE_ERROR = "error"
MESSAGE_EVENT = "event"
MESSAGE_EVENT_DATA = "event_data"
MESSAGE_EVENT_TYPE = "event_type"
MESSAGE_ID = "id"
MESSAGE_SERVICE = "service"
MESSAGE_SERVICE_DATA = "service_data"
MESSAGE_STATE_CHANGED = "state_changed"
MESSAGE_TYPE = "type"
MESSAGE_TYPE_AUTH = "auth"
MESSAGE_TYPE_AUTH_INVALID = "auth_invalid"
MESSAGE_TYPE_AUTH_OK = "auth_ok"
MESSAGE_TYPE_AUTH_REQUIRED = "auth_required"
MESSAGE_TYPE_CALL_SERVICE = "call_service"
MESSAGE_TYPE_EVENT = "event"
MESSAGE_TYPE_GET_CONFIG = "get_config"
MESSAGE_TYPE_GET_SERVICES = "get_services"
MESSAGE_TYPE_GET_STATE = "get_state"
MESSAGE_TYPE_GET_STATES = "get_states"
MESSAGE_TYPE_RESULT = "result"
MESSAGE_TYPE_SUBSCRIBE_EVENTS = "subscribe_events"
MESSAGE_TYPE_SUCCESS = "success"

# Secrets
SECRET_HOME_ASSISTANT_TOKEN = "home_assistant_token"

# Settings
SETTING_AUTOSTART = "autostart"
SETTING_HOME_ASSISTANT_HOST = "home_assistant_host"
SETTING_HOME_ASSISTANT_PORT = "home_assistant_port"
SETTING_HOME_ASSISTANT_SECURE = "home_assistant_secure"
SETTING_LOG_LEVEL = "log_level"

# Models
MODEL_SECRETS = "secrets"
MODEL_SETTINGS = "settings"
