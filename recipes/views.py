from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum

from .models import Recipe, Amount, User, Tag, Purchase
from .forms import RecipeForm
from .business_functions import get_file_content, get_dict_ingredient, get_filters_recipes


def index(request):
    filters, recipes = get_filters_recipes(request)

    tags = Tag.objects.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'page': page,
               'paginator': paginator,
               'tags': tags,
               'filter': filters,
               }

    return render(request, 'index.html', content)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    filters, recipes = get_filters_recipes(request, author=author.id)

    tags = Tag.objects.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'page': page,
               'paginator': paginator,
               'tags': tags,
               'filter': filters,
               'author': author,
               }

    return render(request, 'index.html', content)


@login_required
def favorite(request):
    user = request.user
    filters, recipes = get_filters_recipes(request, favorite__user=user)

    tags = Tag.objects.all()

    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'page': page,
               'paginator': paginator,
               'tags': tags,
               'filter': filters,
               'favorite': True,
               }

    return render(request, 'index.html', content)


@login_required
def purchase(request):
    user = request.user
    purchases = Purchase.objects.filter(user=user).prefetch_related('recipe')

    content = {'purchases': purchases, }

    return render(request, 'recipes/purchase.html', content)


@login_required
def remove_purchase(request, recipe_id):
    user = request.user
    purchase = get_object_or_404(Purchase, recipe=recipe_id, user=user.id)
    purchase.delete()

    return redirect('purchases')


def single_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    ingredients = Amount.objects.filter(recipe=recipe_id)

    content = {'recipe': recipe,
               'ingredients': ingredients,
               }

    return render(request, 'recipes/recipe_page.html', content)


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        ingredients = get_dict_ingredient(request.POST)
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe.tags.set(form.cleaned_data['tags'])

        for ingredient, value in ingredients.items():
            Amount.objects.create(ingredient=ingredient, recipe=recipe, quantity=value)

        return redirect('index')

    context = {'form': form}

    return render(request, 'recipes/form_recipe.html', context)


@login_required
def edit_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)

    if recipe.author != request.user:
        return redirect('recipe', username=username, recipe_id=recipe_id)

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe)

    if form.is_valid():
        ingredients = get_dict_ingredient(request.POST)
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe.tags.set(form.cleaned_data['tags'])
        Amount.objects.filter(recipe_id=recipe.id).delete()
        for ingredient, value in ingredients.items():
            Amount.objects.create(ingredient=ingredient, recipe=recipe, quantity=value)

        return redirect('recipe', username=username, recipe_id=recipe_id)

    ingredients = Amount.objects.filter(recipe=recipe_id)

    active_tags = [tag for tag in recipe.tags.values_list('key', flat=True) if tag]

    context = {'form': form,
               'recipe': recipe,
               'ingredients': ingredients,
               'active_tags': active_tags
               }
    return render(request, 'recipes/form_recipe.html', context)


@login_required
def remove_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


@login_required
def subscriptions(request):
    user = request.user
    authors = User.objects.filter(
        following__user=user).prefetch_related('recipe').order_by('-username')
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator, }

    return render(request, 'recipes/subscription.html', context)


@login_required
def get_purchase(request):
    user = request.user

    purchases_id = Purchase.objects.filter(user=user).values_list('recipe')
    ingredients = Amount.objects.filter(recipe__in=purchases_id) \
        .prefetch_related('ingredient').values(
        'ingredient__title', 'ingredient__dimension').annotate(Sum('quantity'))

    filename, file_content = get_file_content(ingredients, user)

    response = HttpResponse(file_content,
                            content_type='application/text charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response
