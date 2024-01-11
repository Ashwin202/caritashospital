from django import template
from caritasapp.models import Post

register = template.Library()

@register.inclusion_tag('caritasapp/post_list.html')
def display_post_list():
    posts = Post.objects.all()
    return {'posts': posts}
