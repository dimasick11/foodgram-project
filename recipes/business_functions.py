from datetime import datetime

from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe


def get_filters_recipes(request, *args, **kwargs):
    filters = request.GET.getlist('filters')
    if filters:
        recipes = Recipe.objects.filter(
            tags__key__in=filters).filter(**kwargs).distinct()
    else:
        recipes = Recipe.objects.filter(**kwargs).all()

    return filters, recipes


def get_file_content(ingredients, user):
    filename = f'Shopping list from {datetime.now().strftime("%d.%m.%y %H.%M.%S")}.txt'

    file_content = ''
    for ingredient in ingredients:
        ingredient_title = ingredient[
            'ingredient__title'][0].upper() + ingredient[
                'ingredient__title'][1:]
        ingredient_dimension = ingredient['ingredient__dimension']
        quantity_sum = ingredient['quantity__sum']

        file_content += f'• {ingredient_title} ({ingredient_dimension}) — {quantity_sum}\n'
    return filename, file_content


def get_dict_ingredient(request_obj):
    tmp = dict()
    for key in request_obj:
        if key.startswith('nameIngredient'):
            ingredient = get_object_or_404(Ingredient, title=request_obj[key])
            value = key[15:]
            tmp[ingredient] = request_obj['valueIngredient_' + value]
    return tmp


def get_list_ingredients():
    with open('ingredients.csv') as tmp:
        for el in tmp:
            ingr = el.replace('\n', '').split(',')
            mod = Ingredient(title=ingr[0], dimension=ingr[1])
            mod.save()
