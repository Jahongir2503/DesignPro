from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import CustomUserCreationForm


class IndexView(View):
    def get(self, request):
        status = request.GET.get('status', 'all')
        if status != 'all':
            completed_requests = Request.objects.filter(status=status).order_by('-created_at')
        else:
            completed_requests = Request.objects.all().order_by('-created_at')
        in_progress_count = Request.objects.filter(status=Request.IN_PROGRESS).count()
        return render(request, 'index.html',
                      {'completed_requests': completed_requests, 'in_progress_count': in_progress_count})


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class MainPageView(View):
    def get(self, request):
        completed_requests = Request.objects.filter(status=Request.COMPLETED)[:4]
        return render(request, 'main_page.html', {'completed_requests': completed_requests})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')


from django.views.generic.edit import CreateView
from .models import Request


class CreateRequestView(LoginRequiredMixin, CreateView):
    model = Request
    fields = ['title', 'description', 'category', 'photo']
    template_name = 'create_request.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile')


def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class DeleteRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        request_to_delete = get_object_or_404(Request, pk=pk)
        if request.user == request_to_delete.user and request_to_delete.status == Request.NEW:
            request_to_delete.delete()
        return HttpResponseRedirect(reverse('index'))
