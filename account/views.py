import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView, DetailView
from django.contrib.auth.views import LogoutView

# Create your views here.

# class LoginView(FormView):
#     template_name = 'login.html'
#     form_class = ContactForm
#     success_url = '/'
import product
from account.forms import UserRegistrationForm, UserLoginForm, AddressForm, ImageForm
from account.models import User, Address
from order.models import BasketItem, Basket, Order
from product.models import Category


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
        context = {'form': form, 'categories': Category.objects.all()}
        print(form.is_valid())
    else:
        form = UserLoginForm()
        context = {'form': form, 'categories': Category.objects.all()}
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
        context = {'form': form, 'categories': Category.objects.all()}
    else:
        form = UserRegistrationForm()
        context = {'form': form, 'categories': Category.objects.all()}
    return render(request, 'account/register.html', context)


class RegisterView(TemplateView):
    template_name = "account/register.html"


class ProfileView(TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        context['basket'] = Basket.objects.get(user=self.request.user)
        return context


class FullNameView(TemplateView):
    template_name = "account/full_name.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['categories'] = Category.objects.all()
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        context['basket'] = Basket.objects.get(user=self.request.user)
        return context


class AddressView(TemplateView):
    template_name = "account/addresses.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        print('kwargs : ', kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        context['categories'] = Category.objects.all()
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        context['basket'] = Basket.objects.get(user=self.request.user)
        return context


class OrdersView(TemplateView):
    template_name = "account/orders.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        print('kwargs : ', kwargs)
        context['categories'] = Category.objects.all()
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        context['basket'] = Basket.objects.get(user=self.request.user)
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context


@csrf_exempt
def remove_address(request):
    data = json.loads(request.body)
    try:
        Address.objects.get(id=data['address_id']).delete()
        response = {'address_id': data['address_id']}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {'error': 'Error'}
        return HttpResponse(json.dumps(response), status=400)


@csrf_exempt
def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
        print(address)
    return redirect('addresses')


@csrf_exempt
def change_image(request):
    print('before post')
    data = json.loads(request.body)
    if request.method == 'POST':
        print('after post')
        form = ImageForm(request.POST, request.FILES, instance=request.user)
        print('first_form : ', form)
        if form.is_valid():
            form.save()
            print('second_form : ', form)
            response = {'image': form.image.url}
        else:
            response = {'image': form.image.url}
    return HttpResponse(json.dumps(response), status=201)
