from django import template
from blog.models import UserProfile

register = template.Library()


@register.inclusion_tag('blog/get_userinfo_4account.html')   
def get_userinfo(id):
    userinfo = UserProfile.objects.get(user_id = id)
    return {"userinfo": userinfo}