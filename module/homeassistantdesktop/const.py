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
MESSAGE_ID = "id"
MESSAGE_TYPE = "type"
MESSAGE_TYPE_AUTH = "auth"
MESSAGE_TYPE_AUTH_INVALID = "auth_invalid"
MESSAGE_TYPE_AUTH_OK = "auth_ok"
MESSAGE_TYPE_AUTH_REQUIRED = "auth_required"
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
