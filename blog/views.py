from unicodedata import category
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from .forms import UserRegisterForm, UserLoginForm, PostForm
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Category, Tag
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import F  #поможет высчиатать корректно количество просмотров
from django.contrib.auth import login, logout



def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':    #проверка - пришел ли запрос страницы методом POST
        form = UserRegisterForm(request.POST)   #связываем с формой
        if form.is_valid():     #валидация формы, проверка на подлинность
            user = form.save()     #сохраняем пользователя и передаем в переменную user
            login(request, user)    #авторизуем, передавая request и данные пользователя
            messages.success(request, 'Вы успешно прошли регистрацию')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()   #если страница запрошена методом GET,то создаем экземпляр формы, не связанный с данными 
    return render(request, 'blog/register.html', {'form': form})    # {'form': form} передаем контекст в переменную form


def user_login(request):
    if request.method == 'POST':    #проверка - пришел ли запрос страницы методом POST
        form = UserLoginForm(data=request.POST)   #в данном случае просто передать данные не выйдет, необходимо назначить переменную, в которую поместим эти данные
        if form.is_valid():     #валидация формы, проверка на подлинность
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизовались')
            return redirect('home')
    else:
        form = UserLoginForm() #если страница запрошена методом GET,то создаем экземпляр формы, не связанный с данными
    return render(request, 'blog/login.html', {'form': form})   # {'form': form} передаем контекст в переменную form


class Home(ListView):
        model = Post
        template_name = 'blog/index.html'
        context_object_name = 'posts'
        paginate_by = 3         #количество статей на одной сранице

        def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Мой сайт'
            return context


class PostsByCategory(ListView):
        template_name = 'blog/indexCategory.html'
        context_object_name = 'posts'
        paginate_by = 3
        allow_empty = False             #при запросе пустой категории выводило ошибку 404

        def get_queryset(self):
            return Post.objects.filter(category__slug=self.kwargs['slug'])

        def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Статьи по категории: ' + str(Category.objects.get(slug=self.kwargs['slug']))
            return context


class PostsByTag(ListView):
        template_name = 'blog/indexCategory.html'
        context_object_name = 'posts'
        paginate_by = 3
        allow_empty = False             #при запросе пустой категории выводило ошибку 404

        def get_queryset(self):
            return Post.objects.filter(tags__slug=self.kwargs['slug'])

        def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Статьи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
            return context


class GetPost(DetailView):
        model = Post
        template_name = 'blog/single.html'
        context_object_name = 'post'

        def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            self.object.views = F('views') + 1
            self.object.save()
            self.object.refresh_from_db()
            return context


class Search(ListView):
        template_name = 'blog/search.html'
        context_object_name = 'posts'
        paginate_by = 3

        def get_queryset(self):
            return Post.objects.filter(title__icontains=self.request.GET.get('s'))    # icontains - латиница без учетом регистра, а кириллица с учетом

        def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['s'] = f"s={self.request.GET.get('s')}&"
            return context


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm   #связывает данный класс CreateNews с классом формы BlogForm 
    template_name = 'blog/add_news.html'    #указываем существующий template
    # success_url = reverse_lazy('home')      #происходит редирект на главную страницу после добавления новости
    # reverse_lazy в отличии от reverse вызывается после того, как Джанго узнает о существовании маршрута 'home', поэтому не генерит ошибок
    login_url = '/admin'    # 1 способ. Для неавторизованных пользователей ресурс перенаправит на страницу авторизования
    #raise_exception = True     # 2 способ. Для неавторизованных пользователей выдаст ошибку "403 Forbidden"


def indexhome(request):  #контроллер функции стартовой страницы
        return render(request, 'blog/index-home.html')


def get_category(request, slug):        #тестовый вывод страницы
        return render(request, 'blog/category.html')
