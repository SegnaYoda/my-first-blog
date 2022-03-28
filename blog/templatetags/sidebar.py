from turtle import title
from django import template
from blog.models import Post, Tag


register = template.Library()

@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.filter(is_published=True).order_by('-views')[:cnt].select_related('author')
    return {"posts": posts}


@register.inclusion_tag('blog/tags_tpl.html')
def get_tags(cnt=40):
    tags = Tag.objects.all()[:cnt]
    return {"tags": tags}


#для шаблона каетгорий вывод одной популярной новости
@register.inclusion_tag('blog/popular_posts_tpl_single.html')   
def get_popular_single(cnt=1):
    post = Post.objects.filter(is_published=True).order_by('-views')[:cnt].select_related('author')
    return {"post": post}