from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import RecipeViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]