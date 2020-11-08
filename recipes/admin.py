from django.contrib import admin


from .models import Recipe, Ingredient, Amount, Tag, Favorite, Purchase


class AmountInline(admin.TabularInline):
    """Для связывания ингредиентов и колличества"""
    model = Amount
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author')
    search_fields = ('title',)
    list_filter = ('pub_date',)
    date_hierarchy = 'pub_date'
    empty_value_display = '-пусто-'
    inlines = [
        AmountInline,
    ]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)
    
    
@admin.register(Amount)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')
    search_fields = ('recipe',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    
    
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)