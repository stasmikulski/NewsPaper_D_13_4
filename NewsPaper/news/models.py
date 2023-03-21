from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse
from django.core.cache import cache
from profanity.validators import validate_is_profane


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

class Category(models.Model):
    name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='NewsCategory')
    title = models.CharField(max_length=128, validators=[validate_is_profane])
    text = models.TextField(validators=[validate_is_profane])

    rating = models.SmallIntegerField(default=0)
    #slug = models.SlugField(max_length=128, unique=True)

    def datethis(self):
        return self.dateCreation.strftime("%Y-%m-%d %X")

    def datedmy(self):
        return self.dateCreation.strftime("%d-%m-%Y")

    def catz(self):
        #print(self.postCategory.all())
        cats_que = self.postCategory.all()
        catz = []
        for c in cats_que:
            #print(c.name)
            catz.append('#' + c.name)
        #print(catz)
        #catsiinline = ' '.join(catz)
        #print(catsiinline)
        return catz

    def comm_count(self):
        comm_count = Comment.objects.filter(commentPost=self.id).count()
        return comm_count

    def get_absolute_url(self):
        if self.categoryType == 'NW':
            return reverse('post_detail_show', kwargs={'id':self.id})
        if self.categoryType == 'AR':
            return reverse('post_detail_show_ar', kwargs={'id':self.id})

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:19] + '...'
        #return '{} ... {}'.format(self.text[0:123], str(self.rating))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    def __str__(self):
        return f'{self.title} :: {self.text[:20]}'

class NewsCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    CategoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(validators=[validate_is_profane])
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def datethis(self):
        return self.dateCreation.strftime("%Y-%m-%d %X")

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[:30]}'


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
