from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LogoutView

# Create your views here.

# class LoginView(FormView):
#     template_name = 'login.html'
#     form_class = ContactForm
#     success_url = '/'
from account.forms import UserRegistrationForm, UserLoginForm
from account.models import User


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        print("form : ", form)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('home')
        else:
            pass
        context = {'form': form}
        print(form.is_valid())
    else:
        form = UserLoginForm()
        context = {'form': form}
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


class LogoutView(LogoutView):
    redirect_field_name = '/login/'

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            # user = form.save(commit=False)
            # password = user.password
            # user.set_password(password)
            # user.save()
            return redirect('login')
        else:
            pass
        context = {'form': form}
    else:
        form = UserRegistrationForm()
        context = {'form': form}
    return render(request, 'account/register.html', context)


class RegisterView(TemplateView):
    template_name = "account/register.html"
