import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.db.models import Exists, OuterRef
from django_apscheduler import util

from news.models import Post, Category, User
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


def my_job():
    one_week_ago = datetime.today() - timedelta(days=7)
    postnewsweekly = Post.objects.filter(dateCreation__gte=one_week_ago)
    #print(postnewsweekly)
    categoriesall = Category.objects.all()
    #print(categoriesall)
    for cat_here in categoriesall:
        print('  --- SCHEDULER ---', cat_here)
        postnewsweeklycats = Post.objects.filter(dateCreation__gte=one_week_ago, postCategory=cat_here)
        text4email = ''
        html4email = ''
        for p in postnewsweeklycats:
            text4email += (f'Заголовок: {p.title}\n' \
                           f'Ссылка на статью: http://127.0.0.1:8000{p.get_absolute_url()}\n')
            html4email += (f'Заголовок: {p.title}<br>'
                           f'<a href="http://127.0.0.1:8000{p.get_absolute_url()}">'
                           f'Ссылка на статью</a><br>')
        print(text4email)
        print(html4email)


        emails = User.objects.filter(
            subscriptions__category=cat_here
        ).values_list('email', flat=True)

        subject = f'Все новости за неделю в категории {cat_here}'

        for email in emails:
            msg = EmailMultiAlternatives(subject, text4email, None, [email])
            msg.attach_alternative(html4email, "text/html")
            msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")