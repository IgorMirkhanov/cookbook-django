from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'recipes_added', 'favorites_count', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['user__username', 'bio', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'avatar', 'bio')
        }),
        ('Контактная информация', {
            'fields': ('location', 'birth_date', 'website', 'phone')
        }),
        ('Статистика', {
            'fields': ('recipes_added', 'favorites_count')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )