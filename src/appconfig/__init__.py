from .appconfig import AppConfig

APPCONFIG_UPLOAD_PATH_DEFAULT = "appconfig/{appname}/{fieldname}"
APPCONFIG_CAN_CONFIG_DEFAULT = lambda user: user.is_superuser

config = AppConfig()

__all__ = [AppConfig, config]
