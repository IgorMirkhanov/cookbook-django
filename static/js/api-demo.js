// API демонстрация для CookBook
class CookBookAPI {
    constructor() {
        this.baseURL = '/api';
    }

    // Получить все рецепты
    async getRecipes() {
        try {
            const response = await fetch(`${this.baseURL}/recipes/`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Ошибка при получении рецептов:', error);
            return null;
        }
    }

    // Получить детали рецепта
    async getRecipeDetail(id) {
        try {
            const response = await fetch(`${this.baseURL}/recipes/${id}/`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Ошибка при получении рецепта:', error);
            return null;
        }
    }

    // Получить категории
    async getCategories() {
        try {
            const response = await fetch(`${this.baseURL}/categories/`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Ошибка при получении категорий:', error);
            return null;
        }
    }

    // Поиск рецептов
    async searchRecipes(query) {
        try {
            const response = await fetch(`${this.baseURL}/recipes/?search=${encodeURIComponent(query)}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Ошибка при поиске:', error);
            return null;
        }
    }

    // Демонстрация работы API
    async demonstrateAPI() {
        console.log('=== CookBook API Demo ===');
        
        // Получаем рецепты
        const recipes = await this.getRecipes();
        if (recipes && recipes.results) {
            console.log('📚 Всего рецептов:', recipes.count);
            console.log('📖 Первые 3 рецепта:', recipes.results.slice(0, 3));
        }

        // Получаем категории
        const categories = await this.getCategories();
        if (categories && categories.results) {
            console.log('🏷️ Категории:', categories.results);
        }

        // Если есть рецепты, получаем детали первого
        if (recipes && recipes.results && recipes.results.length > 0) {
            const firstRecipeId = recipes.results[0].id;
            const recipeDetail = await this.getRecipeDetail(firstRecipeId);
            console.log('🔍 Детали первого рецепта:', recipeDetail);
        }
    }
}

// Создаем демо-интерфейс на главной странице
function createAPIDemoSection() {
    // Проверяем, не добавлена ли уже секция
    if (document.querySelector('.api-demo')) {
        return;
    }

    const apiDemoHTML = `
        <section class="api-demo" style="background: #f8f9fa; padding: 40px 0; margin: 40px 0; border-top: 1px solid #ddd;">
            <div class="container">
                <h2 style="text-align: center; margin-bottom: 30px; color: #2c3e50;">🎯 API Демонстрация</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="api-card" style="background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h3 style="color: #e74c3c; margin-bottom: 20px;">📚 Эндпоинты API</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li style="margin: 15px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                                <strong>GET /api/recipes/</strong>
                                <br><small style="color: #666;">Список всех рецептов в JSON</small>
                            </li>
                            <li style="margin: 15px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                                <strong>GET /api/recipes/1/</strong>
                                <br><small style="color: #666;">Детали конкретного рецепта</small>
                            </li>
                            <li style="margin: 15px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                                <strong>GET /api/categories/</strong>
                                <br><small style="color: #666;">Список категорий</small>
                            </li>
                        </ul>
                    </div>
                    <div class="api-test" style="background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h3 style="color: #e74c3c; margin-bottom: 20px;">🧪 Тестирование API</h3>
                        <button onclick="testAPI()" style="background: #e74c3c; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; margin: 10px 0; font-size: 16px; transition: background 0.3s ease;">
                            Протестировать API
                        </button>
                        <div id="api-result" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; display: none;">
                            <strong style="color: #2c3e50;">Результат:</strong>
                            <pre id="api-output" style="background: white; padding: 15px; border-radius: 5px; overflow-x: auto; margin-top: 10px; border: 1px solid #ddd; font-size: 12px;"></pre>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 25px;">
                    <a href="/api/recipes/" target="_blank" style="color: #e74c3c; text-decoration: none; font-weight: bold; padding: 10px 20px; border: 2px solid #e74c3c; border-radius: 5px; transition: all 0.3s ease;">
                        🔗 Открыть API в браузере
                    </a>
                </div>
            </div>
        </section>
    `;
    
    // Добавляем секцию после features или перед футером
    const featuresSection = document.querySelector('.features');
    const quickStatsSection = document.querySelector('.quick-stats');
    
    if (featuresSection) {
        featuresSection.insertAdjacentHTML('afterend', apiDemoHTML);
    } else if (quickStatsSection) {
        quickStatsSection.insertAdjacentHTML('afterend', apiDemoHTML);
    } else {
        // Если нет секций, добавляем перед футером
        const main = document.querySelector('main');
        if (main) {
            main.insertAdjacentHTML('beforeend', apiDemoHTML);
        }
    }
}

// Функция для тестирования API
async function testAPI() {
    const api = new CookBookAPI();
    const resultDiv = document.getElementById('api-result');
    const outputDiv = document.getElementById('api-output');
    const button = event.target;
    
    // Показываем загрузку
    resultDiv.style.display = 'block';
    outputDiv.textContent = '🔄 Тестируем API...';
    button.textContent = 'Тестируем...';
    button.disabled = true;
    
    try {
        const recipes = await api.getRecipes();
        const categories = await api.getCategories();
        
        const result = {
            status: '✅ API работает корректно',
            recipes_count: recipes?.count || 0,
            categories_count: categories?.count || 0,
            sample_recipe: recipes?.results?.[0] ? {
                id: recipes.results[0].id,
                title: recipes.results[0].title,
                cooking_time: recipes.results[0].cooking_time
            } : 'Нет рецептов',
            sample_category: categories?.results?.[0] || 'Нет категорий',
            endpoints: {
                recipes: '/api/recipes/',
                categories: '/api/categories/'
            }
        };
        
        outputDiv.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        outputDiv.textContent = '❌ Ошибка: ' + error.message + '\n\nПроверьте:\n1. Запущен ли сервер\n2. Установлен ли DRF\n3. Есть ли данные в БД';
    } finally {
        button.textContent = 'Протестировать API';
        button.disabled = false;
    }
}

// Валидация формы поиска
function setupSearchValidation() {
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[type="text"]');
        if (searchInput) {
            searchInput.addEventListener('input', function(e) {
                if (this.value.length > 100) {
                    this.value = this.value.substring(0, 100);
                    alert('Поисковый запрос не должен превышать 100 символов');
                }
            });
        }
    }
}

// Динамическое обновление счетчика рецептов
function updateRecipeCounter() {
    const recipeCards = document.querySelectorAll('.recipe-card');
    if (recipeCards.length > 0) {
        const counter = document.createElement('div');
        counter.style.cssText = 'position: fixed; top: 80px; right: 20px; background: #e74c3c; color: white; padding: 10px; border-radius: 5px; z-index: 1000;';
        counter.textContent = `📚 Рецептов на странице: ${recipeCards.length}`;
        document.body.appendChild(counter);
        
        setTimeout(() => {
            counter.remove();
        }, 3000);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Добавляем секцию API демонстрации только на главной странице
    if (window.location.pathname === '/') {
        createAPIDemoSection();
    }
    
    // Настраиваем валидацию форм
    setupSearchValidation();
    
    // Обновляем счетчик рецептов на страницах с рецептами
    if (window.location.pathname.includes('/recipes')) {
        updateRecipeCounter();
    }
    
    // Автоматическое тестирование API в консоли
    const api = new CookBookAPI();
    api.demonstrateAPI();
    
    console.log('🚀 CookBook JavaScript загружен!');
    console.log('📖 Доступные функции: testAPI(), CookBookAPI');
});