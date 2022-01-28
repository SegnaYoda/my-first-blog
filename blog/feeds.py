from pydoc import describe
#RSS

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from blog.models import Post
from django.urls import reverse


class LatestPostsFeed(Feed):
    title = "Мой блог"
    link = "/"
    description = "Последние статьи из моего блога."

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)