from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .filters import PostFilter
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def index(request):
    news = Post.objects.all().order_by("dateCreation").reverse()
    # news = Post.objects.all().order_by("-id")
    return render(request, 'index.html', context={'news': news})

def detail(request, id):
    new = Post.objects.get(id=id)
    post_comments = Comment.objects.filter(commentPost=Post.objects.get(id=id))
    post_comments_count = Comment.objects.filter(commentPost=Post.objects.get(id=id)).count()
    #post_comments_values = post_comments.values('dateCreation', 'commentUser', 'rating', 'text')
    #print(post_comments_values)
    return render(request, 'details.html', context={'new': new, 'post_comments': post_comments, 'post_comments_count': post_comments_count})

class PostList(ListView):
   model = Post
   ordering = '-dateCreation'
   template_name = 'index.html'
   context_object_name = 'news'
   paginate_by = 5


class PostSearch(ListView):
   model = Post
   ordering = '-dateCreation'
   template_name = 'search.html'
   context_object_name = 'news'
   paginate_by = 5

   # Переопределяем функцию получения списка новостей
   def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список новостей
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context

class PostDetail(DetailView):
   model = Post
   template_name = 'detail.html'
   context_object_name = 'new'

class PostDetailEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.post_edit',)
    form_class = PostForm
    model = Post
    context_object_name = 'new'
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.save()
        return super(PostDetailEdit, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('detail', kwargs={'id': self.object.pk})

class ArticleDetailEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.article_edit',)
    form_class = PostForm
    model = Post
    context_object_name = 'new'
    template_name = 'article_edit.html'

    def form_valid(self, form):
        #post = form.save(commit=False)
        #post.categoryType = 'AR'
        #Это если будет нужно сменить 'NW' на 'AR'
        form.save()
        return super(ArticleDetailEdit, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('detail', kwargs={'id': self.object.pk})

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.post_delete',)
    model = Post
    context_object_name = 'new'
    template_name = 'post_delete.html'
    success_url = '/news_list/'

class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.article_delete',)
    model = Post
    context_object_name = 'new'
    template_name = 'article_delete.html'
    success_url = '/news_list/'

def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            #form.save()
            return HttpResponseRedirect('/news_list/')
    return render(request, 'post_edit.html', {'form': form})


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.post_create',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        #print('* * * * * * *', self.object.pk)
        return reverse('detail', kwargs={'id': self.object.pk})

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.article_create',)
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('detail', kwargs={'id': self.object.pk})


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        print(category_id)
        category = Category.objects.get(id=category_id)
        print(category)
        action = request.POST.get('action')
        print(action)

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )