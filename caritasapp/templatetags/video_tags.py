from django import template
from caritasapp.models import Video

register = template.Library()

@register.inclusion_tag('caritasapp/video_list.html')
def display_video_list():
    videos = Video.objects.all()
    return {'videos': videos}
