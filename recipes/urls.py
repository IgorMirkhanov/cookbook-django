from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('popular/', views.popular_recipes, name='popular_recipes'),
    path('favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),
]