from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .forms import UserRegistrationForm
import os

def register_user(request):
    """View для реєстрації користувача"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            admin_subject = f'Новий користувач зареєстрований: {user.username}'
            admin_message = f"""
            Новий користувач зареєструвався на сайті.
            
            Дані користувача:
            Ім'я: {user.username}
            Email: {user.email}
            Дата реєстрації: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@example.com')
            
            try:
                send_mail(
                    subject=admin_subject,
                    message=admin_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Помилка відправки листа адміну: {e}")
            
            try:
                context = {
                    'username': user.username,
                    'email': user.email,
                    'registration_date': user.date_joined,
                    'site_name': 'Наш сайт',
                }
                
                html_content = render_to_string(
                    'emails/user_welcome.html',
                    context
                )
                
                user_email = EmailMessage(
                    subject='Ласкаво просимо на наш сайт!',
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                
                user_email.content_subtype = "html"
                
                user_email.cc = [admin_email]  
                
                user_email.send(fail_silently=False)
                
            except Exception as e:
                print(f"Помилка відправки листа користувачу: {e}")
            
            messages.success(
                request,
                f'Користувача {user.username} успішно зареєстровано! '
                f'Перевірте вашу пошту {user.email} для підтвердження.'
            )
            
            return redirect('register')
    
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})