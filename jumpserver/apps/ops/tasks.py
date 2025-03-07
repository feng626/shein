# coding: utf-8
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask

from common.utils import get_logger
from ops.celery import app
from orgs.utils import tmp_to_org
from .celery.decorator import after_app_ready_start
from .celery.utils import (
    create_or_update_celery_periodic_tasks, get_celery_periodic_task,
    disable_celery_periodic_task, delete_celery_periodic_task
)

logger = get_logger(__file__)


def _run_ops_job_execution(execution):
    try:
        with tmp_to_org(execution.org):
            execution.start()
    except SoftTimeLimitExceeded:
        execution.set_error('Run timeout')
        logger.error("Run adhoc timeout")
    except Exception as e:
        execution.set_error(e)
        logger.error("Start adhoc execution error: {}".format(e))


@shared_task(
    verbose_name=_('Clear celery periodic tasks'),
    description=_(
        "At system startup, clean up celery tasks that no longer exist"
    )
)
@after_app_ready_start
def clean_celery_periodic_tasks():
    """清除celery定时任务"""
    logger.info('Start clean celery periodic tasks.')
    register_tasks = PeriodicTask.objects.all()
    for task in register_tasks:
        if task.task in app.tasks:
            continue

        task_name = task.name
        logger.info('Start clean task: {}'.format(task_name))
        disable_celery_periodic_task(task_name)
        delete_celery_periodic_task(task_name)
        task = get_celery_periodic_task(task_name)
        if task is None:
            logger.info('Clean task success: {}'.format(task_name))
        else:
            logger.info('Clean task failure: {}'.format(task))


@shared_task(
    verbose_name=_('Create or update periodic tasks'),
    description=_(
        """With version iterations, new tasks may be added, or task names and execution times may 
        be modified. Therefore, upon system startup, tasks will be registered or the parameters 
        of scheduled tasks will be updated"""
    )
)
@after_app_ready_start
def create_or_update_registered_periodic_tasks():
    from .celery.decorator import get_register_period_tasks
    for task in get_register_period_tasks():
        create_or_update_celery_periodic_tasks(task)
