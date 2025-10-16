from django.core.management.base import BaseCommand
from recipes.models import Recipe, Category

class Command(BaseCommand):
    help = 'Добавляет примеры кулинарных книг-рецептов'

    def handle(self, *args, **options):
        # Создаем категории
        categories = [
            "Супы", "Салаты", "Основные блюда", "Десерты", 
            "Выпечка", "Национальная кухня", "Здоровое питание"
        ]
        
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
        
        # Примеры книг-рецептов
        books_data = [
            {
                'title': 'Итальянская кухня: Паста и не только',
                'description': 'Классические итальянские рецепты от шеф-повара',
                'ingredients': 'паста, томаты, базилик, оливковое масло, чеснок',
                'cooking_steps': '1. Сварить пасту\n2. Приготовить соус\n3. Смешать и подавать',
                'cooking_time': 30,
                'categories': ['Основные блюда', 'Национальная кухня']
            },
            {
                'title': 'Восточные сладости: Десерты Турции',
                'description': 'Аутентичные турецкие десерты с пошаговыми рецептами',
                'ingredients': 'мука, мед, орехи, масло, специи',
                'cooking_steps': '1. Приготовить тесто\n2. Добавить начинку\n3. Выпекать до золотистой корочки',
                'cooking_time': 60,
                'categories': ['Десерты', 'Выпечка', 'Национальная кухня']
            },
            {
                'title': 'Здоровые салаты на каждый день',
                'description': 'Полезные и вкусные салаты для правильного питания',
                'ingredients': 'овощи, зелень, оливковое масло, лимонный сок',
                'cooking_steps': '1. Нарезать овощи\n2. Приготовить заправку\n3. Смешать ингредиенты',
                'cooking_time': 15,
                'categories': ['Салаты', 'Здоровое питание']
            },
            {
                'title': 'Домашняя выпечка: От хлеба до тортов',
                'description': 'Рецепты домашней выпечки для начинающих и опытных',
                'ingredients': 'мука, дрожжи, яйца, молоко, сахар',
                'cooking_steps': '1. Замесить тесто\n2. Дать подойти\n3. Выпекать',
                'cooking_time': 120,
                'categories': ['Выпечка']
            }
        ]
        
        for book in books_data:
            recipe, created = Recipe.objects.get_or_create(
                title=book['title'],
                defaults={
                    'description': book['description'],
                    'ingredients': book['ingredients'],
                    'cooking_steps': book['cooking_steps'],
                    'cooking_time': book['cooking_time']
                }
            )
            
            # Добавляем категории
            for cat_name in book['categories']:
                category = Category.objects.get(name=cat_name)
                recipe.categories.add(category)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Добавлена книга: {book["title"]}')
                )