from django.urls import path

from . import views


urlpatterns = [
    path('ingredients', views.check_ingredient, name='check_ingredient'),
    path('subscriptions', views.add_subscription, name='add_subscription'),
    path('subscriptions/<int:author_id>', views.remove_subscription, name='remove_subscription'),
    path('favorites', views.add_favorites, name='add_faforites'),
    path('favorites/<int:recipe_id>', views.remove_favorites, name='remove_faforites'),
    path('purchases', views.add_purchases, name='add_purchases'),
    path('purchases/<int:recipe_id>', views.remove_purchases, name='remove_purchases'),
]