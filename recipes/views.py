from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum

from .models import Recipe, Amount, User, Tag, Purchase
from .forms import RecipeForm
from .business_functions import file_create, get_dict_ingredient


def index(request):
    filters = request.GET.getlist('filters')

    if filters:
        recipes = Recipe.objects.filter(tags__key__in=filters).distinct()
    else:
        recipes = Recipe.objects.all()

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
    filters = request.GET.getlist('filters')

    if filters:
        recipes = Recipe.objects.filter(tags__key__in=filters, author=author.id).distinct()
    else:
        recipes = Recipe.objects.filter(author=author.id)

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
    filters = request.GET.getlist('filters')

    if filters:
        recipes = Recipe.objects.filter(tags__key__in=filters, favorite_recipe__user=user).distinct()
    else:
        recipes = Recipe.objects.filter(favorite_recipe__user=user)

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

    return render(request, 'purchase.html', content)


@login_required
def remove_purchase(request, recipe_id):
    user = request.user
    purchase = get_object_or_404(Purchase, recipe=recipe_id, user=user.id)
    purchase.delete()

    return redirect('purchases')


def single_recipe(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id, author=author.id)
    ingredients = Amount.objects.filter(recipe=recipe_id)

    content = {'author': author,
               'recipe': recipe,
               'ingredients': ingredients,
               }

    return render(request, 'recipe_page.html', content)


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.POST:
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

    return render(request, 'form_recipe.html', context)


@login_required
def edit_recipe(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id, author=author)

    if author != request.user:
        return redirect('recipe', username=username, recipe_id=recipe_id)

    if request.method == 'POST':
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

    form = RecipeForm(instance=recipe)
    ingredients = Amount.objects.filter(recipe=recipe_id)
    active_tags = [tag.key for tag in recipe.tags.all() if tag]

    context = {'form': form, 'recipe': recipe, 'ingredients': ingredients, 'active_tags': active_tags}
    return render(request, 'form_recipe.html', context)


@login_required
def remove_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


@login_required
def subscriptions(request):
    user = request.user
    authors = User.objects.filter(
        following__user=user).prefetch_related('recipe_author').order_by('-username')
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator, }

    return render(request, 'subscription.html', context)


@login_required
def get_purchase(request):
    user = request.user

    purchases_id_list = Purchase.objects.filter(user=user).values_list('recipe')
    ingredients = Amount.objects.filter(recipe__in=purchases_id_list).prefetch_related('ingredient').values(
        'ingredient__title', 'ingredient__dimension').annotate(Sum('quantity'))

    filename = file_create(ingredients, user.username)

    response = HttpResponse(open(f'files/{filename}', 'rb'), content_type='application/txt')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
