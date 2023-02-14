from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import *

from datetime import datetime, timedelta
one_week_ago = datetime.today() - timedelta(days=1)

# Объяснение про receiver и post_save:
#     Подписчики подписываются не на categoryType (NW и AR), а на рубрики новостей
# типа "Спорт", "Культура" и т.п., а они сохранены не в модели Post, а в модели
# Category, которая доступна из модели Post, используя ManyToManyField через
# модель NewsCategory. К тому же categoryType у Post'а только одна, а postCategory
# может быть несколько одновременно ("Спорт" и "Финансы"), поэтому используем цикл
# for cat_here in categs, там и отправляем письма. Таким образом, если у новости
# две (или больше) категории, и один пользователь подписался на "Спорт", а другой
# на "Финансы", то они оба получат по одному письму. Правда, если один пользователь
# подписался и на "Спорт" и на "Финансы", то он получит два письма с одной статьей.
#     Итак, здесь (внутри функции post_created) поле "Категория" (postCategory) всегда пустое,
# даже при использовании instance.postCategory.through.
# Использовать m2m_changed.connect(post_created, sender=Post.postCategory.through) тоже
# не получается - поле "Категория" (postCategory) опять пустое.
#    Но!
#    Удалось подключить ресивер с m2m_changed, используя в качестве сендера
#    не Post в чистом виде, а Post.postCategory.through
#    Вот так: @receiver(m2m_changed, sender=Post.postCategory.through)
#    Еще задействуем if action == 'post_add'
#    И смотрим ниже, еще ниже
'''
@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return
    if created:
        print('CREATED:', instance.categoryType)
        print(instance.title)
        print(instance.dateCreation)
        print(instance.postCategory.through)

#m2m_changed.connect(post_created, sender=Post.postCategory.through)
'''

@receiver(m2m_changed, sender=Post.postCategory.through)
def changing_categs(sender, instance, action, **kwargs):
    if action == 'pre_add':
        # This will give you the users BEFORE any removals have happened
        print('pre_add:', instance.postCategory.all())
    elif action == 'post_add':
        # This will give you the users AFTER any removals have happened
        print('post_add:', instance.postCategory.all())
        print('CREATED:', instance.categoryType)
        print(instance.title)
        print(instance.dateCreation)

        #for runapscheduler
        postnewsweekly = Post.objects.filter(dateCreation__gte=one_week_ago)
        print(postnewsweekly)
        postnewsweeklycount = Post.objects.filter(dateCreation__gte=one_week_ago).count()
        print(postnewsweeklycount)
        categoriesall = Category.objects.all()
        print(categoriesall)
        for cat in categoriesall:
            print(cat)
            postnewsweeklycats = Post.objects.filter(dateCreation__gte=one_week_ago, postCategory=cat)
            print(postnewsweeklycats)
            postnewsweeklycatscount = Post.objects.filter(dateCreation__gte=one_week_ago, postCategory=cat).count()
            print(postnewsweeklycatscount)
            text4email=''
            html4email=''
            for p in postnewsweeklycats:
                text4email += (f'Заголовок: {p.title}\n' \
                    f'Ссылка на статью: http://127.0.0.1:8000{p.get_absolute_url()}\n')
                html4email += (f'Заголовок: {p.title}<br>' 
                    f'<a href="http://127.0.0.1:8000{p.get_absolute_url()}">'
                    f'Ссылка на статью</a><br>')
            print(text4email)
            print(html4email)
        #for runapscheduler

        categs = instance.postCategory.all()
        print('Categs:', categs)
        for cat_here in categs:
            print('\n- - - - - -', cat_here, '- - - - - -')

            emails = User.objects.filter(
                subscriptions__category=cat_here
            ).values_list('email', flat=True)

            subject = f'New article in category  {cat_here}'
            # subject = f'Новая статья в категории {cat_here}'
    
            text_content = (
                f'Заголовок: {instance.title}\n'
                f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
            )
            html_content = (
                f'Заголовок: {instance.title}<br>'
                f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
                f'Ссылка на статью</a>'
            )
            for email in emails:
                msg = EmailMultiAlternatives(subject, text_content, None, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

