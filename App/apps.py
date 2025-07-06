from django.apps import AppConfig
from django.conf import settings


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'

from django.apps import AppConfig
from django.conf import settings


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'


    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from django_apscheduler.jobstores import DjangoJobStore
        from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
        from App.jobs import move_sailed_data, send_port_update_emails_1, send_port_update_emails_2, send_port_update_emails_3, send_port_update_missed_emails
        import logging
        import os

        logger = logging.getLogger(__name__)

        if os.environ.get('RUN_MAIN') != 'true':
            return

        def job_listener(event):
            if event.exception:
                logger.error('The job crashed :(')
            else:
                logger.info('The job worked fine :)')

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        if not scheduler.get_jobs():
            scheduler.add_job(
                move_sailed_data,
                trigger='cron',
                hour=21,
                minute=59,  
                id='move_sailed_data',
                replace_existing=True
            )

            scheduler.add_job(
                send_port_update_emails_1,
                trigger='cron',
                hour=11,
                minute=30,
                id='send_port_update_emails_1',
                replace_existing=True,
                coalesce=True,
                max_instances=1,
            )

            scheduler.add_job(
                send_port_update_emails_2,
                trigger='cron',
                hour=12,
                minute=30,
                id='send_port_update_emails',
                replace_existing=True,
                coalesce=True,
                max_instances=1,
            )

            scheduler.add_job(
                send_port_update_emails_3,
                trigger='cron',
                hour=13,
                minute=30,
                id='send_port_update_emails_3',
                replace_existing=True,
                coalesce=True,
                max_instances=1,
            )

            scheduler.add_job(
                send_port_update_missed_emails,
                trigger='cron',
                hour=16,
                minute=59,
                id='send_port_update_missed_emails',
                replace_existing=True,
                coalesce=True,
                max_instances=1,
            )

        scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        try:
            scheduler.start()
            logger.info("Scheduler started successfully.")
        except Exception as e:
            logger.error("Scheduler failed to start: %s", str(e))
