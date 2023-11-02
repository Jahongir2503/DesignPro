from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login


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
    return redirect('index')


def main_page(request):
    completed_requests = Request.objects.filter(status=Request.COMPLETED)[:4]
    return render(request, 'main_page.html', {'completed_requests': completed_requests})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
