from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ChangeRequestStatusForm
from .forms import CustomUserCreationForm
from .models import Category
from .models import Request


class IndexView(View):
    def get(self, request):
        status = request.GET.get('status', 'all')
        if status != 'all':
            completed_requests = Request.objects.filter(status=status)
        else:
            completed_requests = Request.objects.all()
        completed_requests = completed_requests.order_by('-created_at')
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
        status = request.GET.get('status', 'all')
        if status != 'all':
            all_requests = Request.objects.filter(status=status)
        else:
            all_requests = Request.objects.all()
        categories = Category.objects.all()
        return render(request, 'admin_dashboard.html', {'requests': all_requests, 'categories': categories})


class CreateRequestView(LoginRequiredMixin, CreateView):
    model = Request
    fields = ['title', 'description', 'category', 'photo']
    template_name = 'create_request.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('profile')


class ChangeRequestStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        request_to_change = get_object_or_404(Request, pk=pk)
        new_status = request.POST.get('status')
        comment = request.POST.get('comment')
        design = request.FILES.get('design')
        if request.user == request_to_change.user:
            request_to_change.change_status(new_status, comment, design)
        return HttpResponseRedirect(reverse('index'))


class DeleteRequestView(LoginRequiredMixin, View):
    def get(self, request, pk):
        request_to_delete = get_object_or_404(Request, pk=pk)
        return render(request, 'confirm_delete.html', {'request': request_to_delete})

    def post(self, request, pk):
        request_to_delete = get_object_or_404(Request, pk=pk)
        if request.user == request_to_delete.user and request_to_delete.status == Request.NEW:
            request_to_delete.delete()
            messages.success(request, 'Заявка успешно удалена.')
        else:
            messages.error(request, 'Вы не можете удалить эту заявку.')
        return HttpResponseRedirect(reverse('profile'))


class AdminDashboardView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        status = request.GET.get('status', 'all')
        if status != 'all':
            all_requests = Request.objects.filter(status=status)
        else:
            all_requests = Request.objects.all()
        categories = Category.objects.all()
        return render(request, 'admin_dashboard.html', {'requests': all_requests, 'categories': categories})


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_new.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser


class ChangeRequestStatusView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Request
    form_class = ChangeRequestStatusForm
    template_name = 'change_request_status.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form = ChangeRequestStatusForm(self.request.POST, self.request.FILES,
                                       instance=self.object)  # Обратите внимание на self.request.FILES
        form.save()
        return super().form_valid(form)
