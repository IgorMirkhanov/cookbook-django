from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    location = models.CharField(max_length=30, blank=True, verbose_name="Местоположение")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    
    # Статистика
    recipes_added = models.PositiveIntegerField(default=0, verbose_name="Добавлено рецептов")
    favorites_count = models.PositiveIntegerField(default=0, verbose_name="Избранных рецептов")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    class Meta:
        app_label = 'users'  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
