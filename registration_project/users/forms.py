from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class UserRegistrationForm(forms.ModelForm):
    """Форма реєстрації користувача"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль',
        min_length=8
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Підтвердження пароля'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Електронна пошта',
        }
    
    def clean_email(self):
        """Валідація email"""
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Це поле обов\'язкове.')
        
        # Перевірка формату email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError('Введіть коректну email адресу.')
        
        # Перевірка на унікальність
        if User.objects.filter(email=email).exists():
            raise ValidationError('Користувач з таким email вже існує.')
        
        return email
    
    def clean(self):
        """Загальна валідація форми, перевірка паролів"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Паролі не співпадають.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Збереження користувача з захешованим паролем"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        
        return user