from .celery_tasks import app as celery_app
　
import logging
　
　
logger = logging.getLogger('django.request')
logger.error("imSupport: Init")
