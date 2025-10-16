from django.shortcuts import render
from recipes.models import Recipe

def index(request):
    featured_recipes = Recipe.objects.all()[:6]  # 6 последних рецептов
    return render(request, 'index.html', {'featured_recipes': featured_recipes})