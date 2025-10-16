from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Recipe, Category, Favorite, Review
from .forms import ReviewForm

def recipe_list(request):
    recipes = Recipe.objects.all()
    categories = Category.objects.all()
    
    # Расширенный поиск
    search_query = request.GET.get('search', '')
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__icontains=search_query)
        )
    
    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        recipes = recipes.filter(categories__id=category_id)
    
    # Фильтрация по времени приготовления
    max_time = request.GET.get('max_time')
    if max_time:
        recipes = recipes.filter(cooking_time__lte=max_time)
    
    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    if sort == 'rating':
        recipes = recipes.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
    elif sort == 'popular':
        recipes = recipes.order_by('-views_count')
    else:
        recipes = recipes.order_by(sort)

    # Получаем ID избранных рецептов пользователя
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)

    # Пагинация
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipe_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'max_time': max_time,
        'sort': sort,
        'user_favorites': list(user_favorites)
    })

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Увеличиваем счетчик просмотров
    recipe.views_count += 1
    recipe.save()

    # Получаем отзывы
    reviews = recipe.review_set.all().order_by('-created_at')

    # Получаем средний рейтинг
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Проверяем, добавлен ли рецепт в избранное
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()

    # Обработка формы отзыва
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            return redirect('recipe_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_favorite': is_favorite,
        'form': form
    })

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )
    if not created:
        favorite.delete()
    return redirect('recipe_detail', pk=recipe_id)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'recipes/favorite_list.html', {'favorites': favorites})

def popular_recipes(request):
    recipes = Recipe.objects.order_by('-views_count')[:6]
    return render(request, 'recipes/popular_recipes.html', {'recipes': recipes})