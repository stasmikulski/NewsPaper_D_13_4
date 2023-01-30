from news.models import *

# 1) Создать двух пользователей
u1 = User.objects.create_user(username='Stanley')
u2 = User.objects.create_user(username='Stayer')
# Создадим еще двух пользователей
u3 = User.objects.create_user(username='Bosch')
u4 = User.objects.create_user(username='Pegeout')
# -- Выведем всех пользователей)
User.objects.all().values('username')
# -- Или любого из них по id
User.objects.get(id=4)

# 2) Создать два объекта модели Author, связанные с пользователями.
Author.objects.create(authorUser=u1)
Author.objects.create(authorUser=u2)
# Author.objects.create(authorUser=u3)
# Author.objects.create(authorUser=u4)
# -- Выведем всех авторов
Author.objects.all().values('authorUser')

# 3) Добавить 4 категории в модель Category.
Category.objects.create(name='IT')
Category.objects.create(name='Politics')
Category.objects.create(name='Sport')
Category.objects.create(name='Education')
# -- Выведем все категории
Category.objects.all().values('name')
# Либо так
#for i in Category.objects.all().values('name'):
#    print(i['name'])

# 4) Добавить 2 статьи и 1 новость.
author = Author.objects.get(id=1)
Post.objects.create(author=author, categoryType='AR', title='Finishing with IBM', text='Equipments for Multi-event tournament by IBM')
author = Author.objects.get(id=2)
Post.objects.create(author=author, categoryType='AR', title='Big Fishing with Hackers', text='Many many comps in far galaxy was damned by hackers')
Post.objects.create(author=author, categoryType='NW', title='To infinity and beyond!', text='A long time ago, in a galaxy far, far away…')
Post.objects.all().values('title')


# 5) Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
Post.objects.get(id=1).postCategory.add(Category.objects.get(id=2))
Post.objects.get(id=2).postCategory.add(Category.objects.get(id=3))
Post.objects.get(id=2).postCategory.add(Category.objects.get(id=4))
# -- Выведем категории
catpost1 = Post.objects.get(id=1).postCategory.all()
catpost1.values('name')
catpost2 = Post.objects.get(id=2).postCategory.all()
catpost2.values('name')

# 6) Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
Comment.objects.create(commentPost=Post.objects.get(id=1),commentUser=Author.objects.get(id=1).authorUser, text='Some text by author')
Comment.objects.create(commentPost=Post.objects.get(id=2),commentUser=Author.objects.get(id=1).authorUser, text='Another text by Big author')
Comment.objects.create(commentPost=Post.objects.get(id=3),commentUser=Author.objects.get(id=2).authorUser, text='Not enough big text by great author')
Comment.objects.create(commentPost=Post.objects.get(id=4),commentUser=Author.objects.get(id=1).authorUser, text='A very small comment from another author')

# 7) Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).dislike()
Comment.objects.get(id=1).rating
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).rating
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).dislike()
Comment.objects.get(id=3).dislike()
Comment.objects.get(id=3).dislike()
Comment.objects.get(id=3).rating
Comment.objects.get(id=4).dislike()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=3).rating
Post.objects.get(id=1).like()
Post.objects.get(id=1).rating
Post.objects.get(id=2).like()
Post.objects.get(id=2).rating
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).rating

# 8) Обновить рейтинги пользователей.
Author.objects.get(id=1).update_rating()
Author.objects.get(id=1).ratingAuthor
Author.objects.get(id=2).update_rating()
Author.objects.get(id=2).ratingAuthor

# 9) Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
authfirst = Author.objects.order_by('-ratingAuthor')[:1]
authfirst[0].ratingAuthor
# Author.objects.get(id=authfirst).ratingAuthor
#? Узнать почему id=authfirst работает как обычный id=3
# authfirstid = authfirst[0].id
# 3
# Author.objects.get(id=authfirstid).ratingAuthor
authfirst[0].authorUser.username
# Author.objects.get(id=authfirst).authorUser.username
# championid = authfirst[0].authorUser.id
# 3
# Author.objects.get(id=championid).authorUser.username

# 10) Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
# -- Если внимательно прочитать, то ищем сначала лучшую статью
postfirst = Post.objects.order_by('-rating')[:1]
# -- Выводим
# Post.objects.get(id=postfirst).dateCreation
Post.objects.get(id=postfirst).dateCreation.strftime("%Y-%m-%d %X")
Post.objects.get(id=postfirst).author.authorUser.username
Post.objects.get(id=postfirst).rating
Post.objects.get(id=postfirst).title
Post.objects.get(id=postfirst).preview()
# ---- Выведем все статьи (кратко)
# Post.objects.all().values('title', 'text', 'rating')
# ---- Выведем все-все комменты (кратко)
# Comment.objects.all().values('text', 'rating')

# 11) Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
# --- Добавим комментарии к посту-чемпиону postfirst
Comment.objects.create(commentPost=Post.objects.get(id=postfirst),commentUser=Author.objects.get(id=2).authorUser, text='Blah-blah-blah - five 555 text by author')
Comment.objects.create(commentPost=Post.objects.get(id=postfirst),commentUser=Author.objects.get(id=3).authorUser, text='Oh, God! 333 letters by 333 writers')
# --- Соберем все комменты к посту-чемпиону postfirst
champ_post_comments = Comment.objects.filter(commentPost=Post.objects.get(id=postfirst))
champ_post_comments_values = champ_post_comments.values('dateCreation', 'commentUser', 'rating', 'text')
# --- Напечатаем их
for i in champ_post_comments_values:
    print(i['dateCreation'].strftime("%Y-%m-%d"), Author.objects.get(id=i['commentUser']).authorUser.username,' Rating:', i['rating'], i['text'])

# *** new, after 23.01.2023
author = Author.objects.get(id=2)
Post.objects.create(author=author, categoryType='AR', title='Reading Famous Lorem Ipsum with Hackers', text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer et porta orci. Integer ullamcorper viverra interdum. Aenean lectus erat, faucibus nec semper vel, venenatis ut diam. Nulla tincidunt eleifend sem venenatis ultricies. Sed et feugiat neque. Etiam elementum non mauris eu rutrum. Fusce faucibus nisl a ex luctus dictum. Etiam feugiat in arcu non ultricies.')
Post.objects.get(id=7).like()
Comment.objects.create(commentPost=Post.objects.get(id=7),commentUser=Author.objects.get(id=2).authorUser, text='Blah-blah-blah - Fishing and Hackers are censored words')
Comment.objects.create(commentPost=Post.objects.get(id=7),commentUser=Author.objects.get(id=2).authorUser, text='Fishing and Hackers are The Greatest words. Amen')
Comment.objects.get(id=10).like()
Comment.objects.get(id=11).like()

# *** new, after 29.01.2023
# from news.models import *
author = Author.objects.get(id=2)
Post.objects.create(author=author, categoryType='AR', title='Amazing Creating Big Text With Short \
Words', text='In Jan 2023 we said - Amazing Creating Big Text With Short Words. Integer et porta orci. \
Integer ullamcorper viverra interdum. Aenean lectus erat, faucibus nec semper vel, venenatis ut diam. Lorem ipsum dolor sit amet, \
consectetur adipiscing elit. Nulla tincidunt eleifend sem venenatis ultricies. Sed et feugiat neque. Etiam elementum non mauris eu rutrum. \
Fusce faucibus nisl a ex luctus dictum. Etiam feugiat in arcu non ultricies.')
Post.objects.all().count()
Post.objects.get(id=8).postCategory.add(Category.objects.get(id=2))
Post.objects.get(id=8).postCategory
Post.objects.get(id=8).like()
Comment.objects.create(commentPost=Post.objects.get(id=8),commentUser=Author.objects.get(id=1).authorUser, text='We are very proud. Long live Rock.n.Roll')
Comment.objects.create(commentPost=Post.objects.get(id=8),commentUser=Author.objects.get(id=3).authorUser, text='God, save the Queen! Show must go on!')
Comment.objects.all().count()
Comment.objects.get(id=12).like()
Comment.objects.get(id=13).like()
Author.objects.get(id=1).update_rating()
Author.objects.get(id=1).ratingAuthor
Author.objects.get(id=2).update_rating()
Author.objects.get(id=2).ratingAuthor
Author.objects.get(id=3).update_rating()
Author.objects.get(id=3).ratingAuthor

Author.objects.create(authorUser=User.objects.get(id=4))
Author.objects.all().values('authorUser')
Author.objects.get(id=4).authorUser.username
author = Author.objects.get(id=4)
Post.objects.create(author=author, categoryType='AR', title='French cars in Big Race-2023 \
Words', text='All french cars, except Citroen C-Crosser runs in Big Race - 2023 in Mercelle, \
In Jan,29,2023. Sed et feugiat neque. Etiam feugiat in arcu non ultricies. Integer ullamcorper \
viverra interdum. Aenean lectus erat, faucibus nec semper vel, venenatis ut diam. Lorem ipsum \
dolor sit amet, consectetur adipiscing elit. Nulla tincidunt eleifend sem venenatis ultricies. \
Etiam elementum non mauris eu rutrum. Fusce faucibus nisl a ex luctus dictum. ')
Post.objects.get(id=9).like()
Comment.objects.create(commentPost=Post.objects.get(id=9),commentUser=Author.objects.get(id=3).authorUser, text='Mitsubishi, Mercedes, Mitsuoka, Mini are not in list?')
Comment.objects.get(id=14).like()

Category.objects.all()
<QuerySet [<Category: name: IT>, <Category: name: Politics>, <Category: name: Sport>, <Category: name: Education>, <Category: name: Culture>]>
Category.objects.create(name='Finance')
1- IT
2- Politics
3- Sport
4- Education
5- Culture
6- Finance

Post.objects.get(id=1).postCategory.all()
1- <QuerySet [<Category: name: Politics>]>
2- <QuerySet [<Category: name: Sport>, <Category: name: Education>]>
3- <QuerySet [<Category: name: Politics>, <Category: name: Sport>]>
4- <QuerySet [<Category: name: Education>, <Category: name: Culture>]>
5- <QuerySet [<Category: name: IT>, <Category: name: Education>]>
6- <QuerySet [<Category: name: Politics>, <Category: name: Finance>]>
7- <QuerySet [<Category: name: Finance>]>
8- <QuerySet [<Category: name: Politics>]>
9- <QuerySet [<Category: name: Sport>]>

Post.objects.get(id=9).postCategory.all()

Post.objects.get(id=6).postCategory.add(Category.objects.get(id=7))
# ^- Случайно добавил не ту категорию

Post.objects.get(id=9).postCategory.filter(name='Finance').delete()
# ^- Удалил ее, НО ОНА УДАЛИЛАСЬ ИЗ КАТЕГОРИЙ ТОЖЕ

Category.objects.create(name='Finance')
7- Finance


Post.objects.get(id=9).postCategory.add(Category.objects.get(id=3))





