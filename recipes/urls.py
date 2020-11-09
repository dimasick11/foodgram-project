from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_recipe, name='create'),
    path('subscription/', views.subscriptions, name='subscriptions'),
    path('favorite/', views.favorite, name='favorites'),
    path('purchase/', views.purchase, name='purchases'),
    path('purchase/download/', views.get_purchase, name='get_purchase'),
    path('purchase/<int:recipe_id>/',
         views.remove_purchase, name='remove_purchase'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/',
         views.single_recipe, name='recipe'),
    path('<str:username>/<int:recipe_id>/edit/',
         views.edit_recipe, name='edit_recipe'),
    path('<str:username>/<int:recipe_id>/remove/',
         views.remove_recipe, name='remove_recipe'),
]
