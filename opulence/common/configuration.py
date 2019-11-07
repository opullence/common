import os
import logging
import logging.config

import yaml
from celery import Celery
from kombu.serialization import register

from . import jsonEncoder

settings = {}

register(
    "customEncoder",
    jsonEncoder.custom_dumps,
    jsonEncoder.custom_loads,
    content_type="application/x-customEncoder",
    content_encoding="utf-8",
)

def get_conf():
    global settings
    return settings

def load_config_from_file(file=None):
    global settings
    config_file = file or os.getenv("CONFIG_FILE", "settings.yml")
    try:
        with open(config_file, "r") as stream:
            settings = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print("Configuration format error:", err)
    except IOError:
        print("IOERROR in load_config_from_file", config_file)
    except Exception as err:
        print("Error while trying to load configuration file", config_file, err)


def configure_celery(config, **kwargs):
    app = Celery(__name__, **kwargs)
    app.conf.update(config)
    app.conf.update(
        {
            "task_routes": ("opulence.common.celery.taskRouter.TaskRouter",),
            "accept_content": ["customEncoder", 'application/json'],
            "task_serializer": "customEncoder",
            "result_serializer": "customEncoder",
        }
    )
    return app


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return settings["log"]["debug"]


LOGFILE = os.path.join(os.getcwd(), "opulence.log")
if hasattr(settings, "log") and "file" in settings["log"]:
    LOGFILE = settings["log"]["file"]


DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {"require_debug_true": {"()": RequireDebugTrue}},
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(name)s %(thread)d %(threadName)s %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": LOGFILE,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "file"], "level": "INFO", "propagate": False}
    },
}

logging.config.dictConfig(DEFAULT_LOGGING)