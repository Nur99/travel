import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.shared_task(default_retry_delay=3, max_retries=2)
def cancel_reservation(reservation_id):
    from .models import Event
    try:
        logger.info("we are here")
    except Exception as e:
        logger.error(str(e))
        raise cancel_reservation.retry(exc=e)
