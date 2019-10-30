import celery

from .exceptions import TaskTimeoutError


def sync_call(app, task_path, timeout, **kwargs):
    try:
        task = app.send_task(task_path, **kwargs)
        return task.get(timeout=timeout)
    except celery.exceptions.TimeoutError:
        raise TaskTimeoutError(f"Task {task_path}")
    except Exception as err:
        print("!!!!!!!!!!!", err)


def async_call(app, task_path, timeout, **kwargs):
    try:
        return app.send_task(task_path, **kwargs)
    except celery.exceptions.TimeoutError:
        raise TaskTimeoutError(f"Task {task_path}")
    except Exception as err:
        print("!!!!!!!!!!!", err)