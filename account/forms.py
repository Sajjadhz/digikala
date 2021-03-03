from django import forms
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from account.models import Address, User
from account.validators import validate_passwords, validate_password, validate_email_login, validate_email_as_username


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label=_('ایمیل'), required=True, help_text=_('ایمیلتون رو وارد کنید'),
                             widget=forms.TextInput(
                                 attrs={"placeholder": "Password", "class": "no-background border-secondary rounded"}))
    password = forms.CharField(label=_('کلمه عبور'),
                               widget=forms.PasswordInput(
                                   attrs={"placeholder": "Password",
                                          "class": "no-background border-secondary rounded"}),
                               required=True)
    password2 = forms.CharField(label=_('تکرار کلمه عبور'), widget=forms.PasswordInput(
        attrs={"placeholder": "Password", "class": "no-background border-secondary rounded"}), required=True)
    first_name = forms.CharField(label=_('نام'), widget=forms.TextInput(
        attrs={"placeholder": "Password", "class": "no-background border-secondary rounded"}))
    last_name = forms.CharField(label=_('نام خانوادگی'), widget=forms.TextInput(
        attrs={"placeholder": "Password", "class": "no-background border-secondary rounded"}))

    def clean(self):
        password1 = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        validate_passwords(password1, password2)

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        validate_email(email)
        validate_email_as_username(email)
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        validate_password(password)
        return password


class UserLoginForm(forms.Form):
    email = forms.CharField(label=_('Email'), max_length=150, required=True, widget=forms.TextInput(
        attrs={"placeholder": "Password", "class": "no-background border-secondary rounded"}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={"placeholder": "Password", "class": "no-background border-secondary rounded"}),
                               required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        validate_email_login(email)
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        validate_password(password)
        return password


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('city', 'street', 'alley', 'zip_code')


class ImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image',)


class EditNameForm(forms.Form):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobile')
        widget = {'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
                  'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
                  'mobile': forms.NumberInput
                  }
        labels = {'first_name': _('نام'),
                  'last_name': _('نام خانوادگی'),
                  'mobile': _('موبایل'),
                  }
