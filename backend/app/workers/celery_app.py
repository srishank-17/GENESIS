from celery import Celery
from app.config import settings

celery_app = Celery(
    "genesis_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_routes={
        "app.workers.document_tasks.*": {"queue": "document_pipeline"},
        "app.workers.embedding_tasks.*": {"queue": "embedding"},
        "app.workers.*": {"queue": "default"},
    }
)

@celery_app.task(name="ping")
def ping():
    return "pong"
