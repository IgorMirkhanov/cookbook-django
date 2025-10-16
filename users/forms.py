from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'avatar', 'website', 'phone']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Расскажите о себе, ваших кулинарных предпочтениях...',
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Город, страна',
                'class': 'form-control'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'https://example.com',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7 (XXX) XXX-XX-XX',
                'class': 'form-control'
            }),
        }
        labels = {
            'bio': 'О себе',
            'location': 'Местоположение',
            'birth_date': 'Дата рождения',
            'avatar': 'Аватар',
            'website': 'Веб-сайт',
            'phone': 'Телефон',
        }