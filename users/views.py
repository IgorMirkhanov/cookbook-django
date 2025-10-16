from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile
from .forms import ProfileUpdateForm
from recipes.models import Recipe, Favorite

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        # Создаем профиль, если его нет
        profile = Profile.objects.create(user=request.user)
        messages.info(request, 'Профиль был создан автоматически.')
    
    user_recipes = Recipe.objects.all()  # В будущем можно фильтровать по автору
    favorites = Favorite.objects.filter(user=request.user)
    
    # Обновляем статистику
    profile.favorites_count = favorites.count()
    profile.save()
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    context = {
        'profile': profile,
        'form': form,
        'user_recipes_count': user_recipes.count(),
        'favorites_count': favorites.count(),
        'favorites': favorites[:3]  # Последние 3 избранных
    }
    return render(request, 'profile.html', context)