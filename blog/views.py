from unicodedata import category
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from django.db.models import F  #поможет высчиатать корректно количество просмотров


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

            


def index(request):  #контроллер функции
        return render(request, 'blog/index.html')


def indexhome(request):  #контроллер функции
        return render(request, 'blog/index-home.html')


def get_category(request, slug):
        return render(request, 'blog/category.html')


def get_post(request, slug):
        return render(request, 'blog/category.html')
