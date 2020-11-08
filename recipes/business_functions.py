from datetime import datetime

from django.shortcuts import get_object_or_404

from .models import Ingredient


def file_create(ingredients, username):
    filename = f'{datetime.now().strftime("%d.%m.%y %H.%M.%S")} {username} purchase\'s.txt'

    with open(f'files/{filename}', 'w') as tmp:
        for ingredient in ingredients:
            ingredient_title = ingredient['ingredient__title'][0].upper() + ingredient['ingredient__title'][1:]
            ingredient_dimension = ingredient['ingredient__dimension']
            quantity_sum = ingredient['quantity__sum']

            tmp_name = f'• {ingredient_title} ({ingredient_dimension}) — {quantity_sum}\n'
            tmp.write(tmp_name)
    return filename


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
        for l in tmp:
            ingr = l.replace('\n', '').split(',')
            mod = Ingredient(title=ingr[0], dimension=ingr[1])
            mod.save()
