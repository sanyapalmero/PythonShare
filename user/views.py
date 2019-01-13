from code.models import Code
from code.views import add_log_entry

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import CreateUserForm
from .models import User


class CreateView(View):
    """Страница регистрации"""

    def get(self, request):
        template_name = 'user/register.html'
        form = CreateUserForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        template_name_login = 'user/login.html'
        template_name_register = 'user/register.html'

        form = CreateUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            avatar = request.FILES.get('avatar')

            user = User.objects.create_user(username, password, avatar)
            good = 'Вы успешно зарегистрированы!'
            return render(request, template_name_login, {'good': good})
        else:
            return render(request, template_name_register, {'form': form})


class LoginView(View):
    """Страница авторизации"""

    def get(self, request):
        template_name = 'user/login.html'
        return render(request, template_name)

    def post(self, request):
        template_name = 'user/login.html'
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('code:index')
        else:
            bad = 'Неверное имя пользователя или пароль'
            add_log_entry(
                request, request.user,
                "Попытка авторизации. Неверное имя пользователя или пароль.")
            return render(request, template_name, {'bad': bad})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('code:index')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """Страница профиля пользователя"""
    ENTRIES_COUNT = 10

    def get(self, request):
        template_name = 'user/profile.html'
        user_codes = Code.objects.filter(user=request.user)
        paginator = Paginator(user_codes, ENTRIES_COUNT)
        page = request.GET.get('page')
        codes = paginator.get_page(page)
        return render(request, template_name, {
            'codes': codes,
            'all': user_codes
        })


@method_decorator(login_required, name='dispatch')
class ProfileSettingsView(View):
    """Страница настроек профиля"""

    def get(self, request):
        template_name = 'user/settings.html'
        return render(request, template_name)


@method_decorator(login_required, name='dispatch')
class UpdateAvatarView(View):
    def post(self, request):
        template_name = 'user/settings.html'
        user = get_object_or_404(User, username=request.user)
        avatar = request.FILES.get('avatar')

        if not avatar:
            error = "Файл не выбран"
            return render(request, template_name, {'bad_avatar': error})
        else:
            user.avatar = avatar
            user.save()
            return redirect('user:profile')


@method_decorator(login_required, name='dispatch')
class UpdatePasswordView(View):
    def post(self, request):
        template_name_login = 'user/login.html'
        template_name_settings = 'user/settings.html'

        user = get_object_or_404(User, username=request.user)
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()

            good = "Пароль успешно был изменен, авторизуйтесь снова."
            add_log_entry(request, request.user, "Успешное изменение пароля")
            return render(request, template_name_login, {'good_pass': good})
        else:
            error = "Пароли не совпадают!"
            add_log_entry(request, request.user,
                          "Попытка изменения пароля: пароли не совпадают")
            return render(request, template_name_settings, {'bad_pass': error})
