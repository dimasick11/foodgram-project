from django.contrib import admin

from .models import Follow


@admin.register(Follow)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "user")
