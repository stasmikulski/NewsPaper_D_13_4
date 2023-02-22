from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
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
from django.core.cache import cache
from django.http import HttpResponse
from django.views import View
from .tasks import hello, my_job

class IndexView(View):
    def get(self, request):
        my_job.delay()
        hello.delay()
        return HttpResponse('Hello!')

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

   queryset = Post.objects.all()
'''
   def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
       obj = cache.get(f'post-{self.kwargs["pk"]}',
                       None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

       # если объекта нет в кэше, то получаем его и записываем в кэш
       if not obj:
           obj = super().get_object(queryset=self.queryset)
           cache.set(f'post-{self.kwargs["pk"]}', obj)

       return obj'''

class PostDetailEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    context_object_name = 'new'
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.save()
        return super(PostDetailEdit, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('post_detail_show', kwargs={'id': self.object.pk})


class ArticleDetailEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
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
        return reverse('post_detail_show', kwargs={'id': self.object.pk})

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    print('- -  - - - >', model.pk)
    print('- -  - - - >', model.id)
    context_object_name = 'new'
    template_name = 'post_delete.html'
    success_url = '/news_list/'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
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
    permission_required = ('news.add_post',)
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
        return reverse('post_detail_show', kwargs={'id': self.object.pk})


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('post_detail_show', kwargs={'id': self.object.pk})

@csrf_protect
@permission_required('news.add_comment',)
def comment_create_view(request, pk):
    # permission_required = ('news.add_comment',) # пока не понятно работает или нет
    # TODO ^- проверить это
    print('- -  - - - >', pk)
    new = Post.objects.get(id=pk)
    print('New:', new)
    if request.method == 'GET':
        #print('GET - - - >', pk)
        comment_form = CommentForm()
        context = {
            'new': new,
            'comment_form': comment_form,
        }
        return render(request, 'comment_create.html', context)

    elif request.method == 'POST':
        #print('POST - - - >', pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #print('POST - - - >form.is_valid', pk)
            commentUser = comment_form.cleaned_data.get('commentUser')
            text = comment_form.cleaned_data.get('text')
            Comment.objects.create(
                commentPost=new,
                commentUser=commentUser,
                text=text
            )
            context = {
                'new': new,
                'comment_form': comment_form,
            }
            return HttpResponseRedirect(reverse('post_detail_show', kwargs={'id' : pk}))
        else:
            context = {
                'new': new,
                'comment_form': comment_form,
            }
            return render(request, 'comment_create.html', context)


class Commen_tCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_comment',)
    # TODO Как здесь вызвать Post по номеру id или pk, если они сюда никак не передаются
    #new = Post.objects.get(id=pk)
    #print('New:', new)
    model = Comment
    form_class = CommentForm
    template_name = 'comment_create.html'
''' не работает:
    def get_object(self):
        obj = super().get_object()
        pk = self.kwargs.get('pk')
        print('   - - - pk - - - ', pk)'''
'''
    def form_valid(self, form):
        print(self.kwargs['pk'])
        if comment_form.is_valid():
            commentUser = comment_form.cleaned_data.get('commentUser')
            text = comment_form.cleaned_data.get('text')
            Comment.objects.create(
                commentPost=new,
                commentUser=commentUser,
                text=text
            )
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        print(self.object.pk)
        return reverse('post_detail_show', kwargs={'id': self.object.pk})
'''

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