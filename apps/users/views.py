from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

User = get_user_model()


def register_view(request):
    errors = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        if password != password_repeat:
            errors['password_repeat'] = 'Паролі не співпадають'

        if User.objects.filter(username=username).exists():
            errors['username'] = 'Такий логін вже існує'

        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('welcome')

    return render(request, 'users/register.html', {'errors': errors})


def login_view(request):
    errors = {}

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('welcome')
        else:
            errors['login'] = 'Невірний логін або пароль'

    return render(request, 'users/login.html', {'errors': errors})


def logout_view(request):
    logout(request)
    return redirect('welcome')


@login_required
def profile_view(request):
    next_url = request.GET.get('next') or 'welcome'

    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.save()
        return redirect(request.POST.get('next') or 'welcome')

    return render(request, 'users/profile.html', {'next_url': next_url})


@login_required
def change_password_view(request):
    errors = {}

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if old_password == new_password1:
            errors['same_password'] = 'Новий пароль не може бути таким самим як старий'

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid() and not errors:
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {
        'form': form,
        'errors': errors,
    })