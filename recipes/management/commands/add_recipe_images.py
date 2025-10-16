from django.core.management.base import BaseCommand
from django.core.files import File
from recipes.models import Recipe
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Добавляет изображения для рецептов'

    def handle(self, *args, **options):
        # Создаем папку для изображений если нет
        media_dir = settings.MEDIA_ROOT / 'recipes'
        media_dir.mkdir(exist_ok=True)

        # Словарь с URL изображений для каждого рецепта
        image_urls = {
            'Итальянская кухня: Паста и не только': 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400&h=300&fit=crop',
            'Восточные сладости: Десерты Турции': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=400&h=300&fit=crop',
            'Здоровые салаты на каждый день': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop',
            'Домашняя выпечка: От хлеба до тортов': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop'
        }

        for title, image_url in image_urls.items():
            try:
                recipe = Recipe.objects.get(title=title)
                if not recipe.image:  # Добавляем только если нет изображения
                    # Скачиваем и сохраняем изображение
                    import requests
                    from io import BytesIO
                    
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_name = f"{title.replace(' ', '_').replace(':', '')}.jpg"
                        image_path = media_dir / image_name
                        
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        
                        with open(image_path, 'rb') as f:
                            recipe.image.save(image_name, File(f), save=True)
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'Добавлено изображение для: {title}')
                        )
                        
                        # Удаляем временный файл
                        os.remove(image_path)
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Не удалось скачать изображение для: {title}')
                        )
            except Recipe.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Рецепт не найден: {title}')
                )