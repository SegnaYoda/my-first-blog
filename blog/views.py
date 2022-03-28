from unicodedata import category
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
# Create your views here.
from .forms import CommentForm, UserRegisterForm, UserLoginForm, PostForm
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from .models import Post, Category, Tag, UserProfile
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import F  # поможет высчиатать корректно количество просмотров
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import PostEditForm



class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)


def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':  # проверка - пришел ли запрос страницы методом POST
        form = UserRegisterForm(request.POST)  # связываем с формой
        if form.is_valid():  # валидация формы, проверка на подлинность
            user = form.save()  # сохраняем пользователя и передаем в переменную user
            # авторизуем, передавая request и данные пользователя
            login(request, user)
            messages.success(request, 'Вы успешно прошли регистрацию')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        # если страница запрошена методом GET,то создаем экземпляр формы, не связанный с данными
        form = UserRegisterForm()
    # {'form': form} передаем контекст в переменную form
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':  # проверка - пришел ли запрос страницы методом POST
        # в данном случае просто передать данные не выйдет, необходимо назначить переменную, в которую поместим эти данные
        form = UserLoginForm(data=request.POST)
        if form.is_valid():  # валидация формы, проверка на подлинность
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизовались')
            return redirect('home')
    else:
        # если страница запрошена методом GET,то создаем экземпляр формы, не связанный с данными
        form = UserLoginForm()
    # {'form': form} передаем контекст в переменную form
    return render(request, 'blog/login.html', {'form': form})


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 3  # количество статей на одной сранице

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('author', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class PostsByCategory(ListView):
    template_name = 'blog/indexCategory.html'
    context_object_name = 'posts'
    paginate_by = 3
    allow_empty = False  # при запросе пустой категории выводило ошибку 404

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'], is_published=True).select_related('author', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи по категории: ' + \
            str(Category.objects.get(slug=self.kwargs['slug']))
        return context


class PostsByTag(ListView):
    template_name = 'blog/indexCategory.html'
    context_object_name = 'posts'
    paginate_by = 3
    allow_empty = False  # при запросе пустой категории выводило ошибку 404

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'], is_published=True).select_related('author', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи по тегу: ' + \
            str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class GetPost(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'
    form_class = CommentForm
    success_msg = 'Комментарий отправлен.'      # вывод об успехе отправки коммента

    def get_success_url(self, **kwargs):    # обновление страницы
        return reverse_lazy('post', kwargs={'slug': self.get_object().slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = UserProfile.objects.get(user=self.request.user)
        self.object.save()
        return super().form_valid(form)


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        # icontains - латиница без учетом регистра, а кириллица с учетом
        return Post.objects.filter(title__icontains=self.request.GET.get('s'), is_published=True).select_related('author', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['result'] = self.request.GET.get('s')
        return context


def indexhome(request):  # контроллер функции стартовой страницы
    return render(request, 'blog/index-home.html')


def personalaccount(request):  # контроллер функции стартовой страницы
    return render(request, 'blog/personalaccount.html')


def get_category(request, slug):
    return render(request, 'blog/category.html')


def rssfeed(request):
    return render(request, 'blog/rss-parsing.html')



def add_post(request):
    post_form= PostEditForm(request.POST)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():     #прошла ли форма валидацию
            object = form.save(commit=False)
            object.author = UserProfile.objects.get(user=request.user)
            object.save()
            img_obj = form.instance
            context = {"img_obj": img_obj}
            return redirect('home')
    else:
        form = PostForm()
    context = {
        "form": form,
        "post_form" : post_form, }
    return render(request, 'blog/add_post.html', context)

