from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse

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
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
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
            catdies = '#' + c.name
            catz.append(catdies)
        #print(catz)
        #catsiinline = ' '.join(catz)
        #print(catsiinline)
        return catz

    def get_absolute_url(self):
        return reverse('detail', kwargs={'id':self.id})

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:19] + '...'
        #return '{} ... {}'.format(self.text[0:123], str(self.rating))

    def __str__(self):
        return f'{self.title}: {self.text[:20]}'

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    CategoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
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
