from django import template

from users.models import Follow
from recipes.models import Favorite, Purchase

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter(name='filter_recipes')
def filter_recipes(request, tag):
    request_add = request.GET.copy()

    if tag.key in request.GET.getlist('filters'):
        filters = request_add.getlist('filters')
        filters.remove(tag.key)
        request_add.setlist('filters', filters)
    else:
        request_add.appendlist('filters', tag.key)
    
    return request_add.urlencode()


@register.filter(name='check_following')
def check_following(author, user):
    result = Follow.objects.filter(author=author.id, user=user.id).exists()
    return result


@register.filter(name='get_suffix_recipe')
def get_suffix_recipe(amount):
    tmp = str(amount - 3)
    if tmp[-1] == 1:
        return '1 рецепт'
    elif tmp[-1] in [2, 3, 4]:
        return f'{tmp} рецепта'
    return f'{tmp} рецептов'


@register.filter(name='check_favorites')
def check_favorites(user, recipe):
    result = Favorite.objects.filter(user=user, recipe=recipe).exists()
    return result


@register.filter(name='check_purchase')
def check_purchase(user, recipe):
    result = Purchase.objects.filter(user=user, recipe=recipe).exists()
    return result


@register.filter(name='get_count_purchase')
def get_count_purchase(user):
    result = Purchase.objects.filter(user=user).count()
    return result
