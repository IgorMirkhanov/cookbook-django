from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Create profiles for all users without profiles'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(
                self.style.SUCCESS(f'Created profile for {user.username}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('All users now have profiles!')
        )