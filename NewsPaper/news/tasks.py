from celery import shared_task
import time
from news.models import Post, Category, User
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def my_job():
    one_week_ago = datetime.today() - timedelta(days=7)
    postnewsweekly = Post.objects.filter(dateCreation__gte=one_week_ago)
    print(postnewsweekly)
    categoriesall = Category.objects.all()
    print(categoriesall)
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