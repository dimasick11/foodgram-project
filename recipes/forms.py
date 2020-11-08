from django.forms import ModelForm, CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'time', 'description', 'image']
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }