from django import template
from blog.models import Post, Tag


register = template.Library()

@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {"posts": posts}


@register.inclusion_tag('blog/tags_tpl.html')
def get_tags(cnt=30):
    tags = Tag.objects.all()[:cnt]
    return {"tags": tags}


#для шаблона каетгорий вывод одной популярной новости
@register.inclusion_tag('blog/popular_posts_tpl_single.html')   
def get_popular_single(cnt=1):
    post = Post.objects.order_by('-views')[:cnt]
    return {"post": post}