from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .filters import PostFilter
from .forms import *


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
   paginate_by = 3


class PostSearch(ListView):
   model = Post
   ordering = '-dateCreation'
   template_name = 'search.html'
   context_object_name = 'news'
   paginate_by = 2

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

class PostDetailEdit(UpdateView):
    form_class = PostForm
    model = Post
    context_object_name = 'new'
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.save()
        return super(PostDetailEdit, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('detail', kwargs={'id': self.object.pk})

class ArticleDetailEdit(UpdateView):
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

class PostDelete(DeleteView):
    model = Post
    context_object_name = 'new'
    template_name = 'post_delete.html'
    success_url = '/news_list/'

class ArticleDelete(DeleteView):
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


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('detail', kwargs={'id': self.object.pk})

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('detail', kwargs={'id': self.object.pk})