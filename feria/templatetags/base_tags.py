from django import template
import feria.models as models

register = template.Library()


@register.simple_tag
def public_forums():
    return list(models.Forum.objects.filter(public=True))
