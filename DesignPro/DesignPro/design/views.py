from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import CustomUserCreationForm
from .models import Request


# Эта функция будет отвечать за отображение начальной страницы
def index(request):
    # Здесь мы используем функцию render, чтобы отобразить наш шаблон index.html
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  # Убедитесь, что этот метод вызывается
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def main_page(request):
    completed_requests = Request.objects.filter(status=Request.COMPLETED)[:4]
    return render(request, 'main_page.html', {'completed_requests': completed_requests})
