import logging.config
import os

import yaml
from celery import Celery
from kombu.serialization import register

from . import jsonEncoder

CONFIG_FILENAME = os.getenv("CONFIG_FILE", "settings.yml")
config = {}


register(
    "customEncoder",
    jsonEncoder.custom_dumps,
    jsonEncoder.custom_loads,
    content_type="application/x-customEncoder",
    content_encoding="utf-8",
)


try:
    with open(CONFIG_FILENAME, "r") as stream:
        config = yaml.safe_load(stream)
except yaml.YAMLError as err:
    print("Configuration format error:", err)
except IOError:
    pass
except Exception as err:
    print("Error while trying to load configuration file", err)


def configure_celery(config, **kwargs):
    app = Celery(__name__, **kwargs)
    app.conf.update(config)
    app.conf.update(
        {
            "task_routes": ("opulence.common.celery.taskRouter.TaskRouter",),
            "accept_content": ["customEncoder"],
            "task_serializer": "customEncoder",
            "result_serializer": "customEncoder",
        }
    )
    return app


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return config["log"]["debug"]


LOGFILE = os.path.join(os.getcwd(), "opulence.log")
if "file" in config["log"]:
    LOGFILE = config["log"]["file"]


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
