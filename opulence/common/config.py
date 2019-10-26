import os

import yaml
from celery import Celery
from kombu.serialization import register

from . import jsonEncoder

register(
    "mongoEncoder",
    jsonEncoder.custom_dumps,
    jsonEncoder.custom_loads,
    content_type="application/x-mongoEncoder",
    content_encoding="utf-8",
)

config = {}


def load_config_from_file(filename):
    global config

    module_path = os.path.abspath(__file__)
    for loc in os.path.dirname(module_path), os.curdir, os.path.expanduser("~"):
        try:
            with open(os.path.join(loc, filename), "r") as stream:
                config = yaml.safe_load(stream)
            break
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
            "task_routes": ("common.utils.tasks.TaskRouter",),
            "accept_content": ["mongoEncoder"],
            "task_serializer": "mongoEncoder",
            "result_serializer": "mongoEncoder",
        }
    )
    return app
