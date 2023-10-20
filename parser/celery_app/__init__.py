from config.config import config
from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    # In the code snippet provided, `"celery_app"` is the name given to the Celery application. It is
    # used to identify and refer to the Celery application throughout the code.
    "celery_app",
    backend=config.CELERY_BACKEND_URL,
    broker=config.CELERY_BROKER_URL,
)

# The line `celery_app.conf.imports = ["celery_app.tasks.tasks"]` is importing the tasks module into
# the Celery app configuration. This allows the Celery app to discover and register the tasks defined
# in the `celery_app.tasks.tasks` module, so that they can be executed by the Celery workers.
celery_app.conf.imports = [
    "celery_app.tasks.tasks"
]
# `celery_app.conf.task_routes` is configuring the routing of tasks in Celery.
celery_app.conf.task_routes = {"celery_app.celery_worker.test_celery": "test-queue"}
# The line `celery_app.conf.update(task_track_started=True)` is updating the Celery app configuration
# to enable tracking of task start events. When `task_track_started` is set to `True`, Celery will
# emit a `task-started` event when a task is started. This event can be used for monitoring and
# tracking the progress of tasks.
celery_app.conf.update(task_track_started=True)
# The code `celery_app.conf.beat_schedule` is configuring the periodic tasks to be executed by the
# Celery beat scheduler.
celery_app.conf.beat_schedule = {
    'run-every-1-minute': {
        'task': 'get_and_write_weather',
        'schedule': crontab(minute='*/1'),
    },
}
