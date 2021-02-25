from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('First name'), max_length=60, null=True)
    last_name = models.CharField(_('Last name'), max_length=60, null=True)
    email = models.EmailField(_('Email'), max_length=100, db_index=True, unique=True)
    password = models.CharField(_('Password'), max_length=150)
    mobile = models.CharField(_('Mobile'), blank=True, max_length=150)
    image = models.ImageField(_('Image'), upload_to='users/image')
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Address(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='addresses', related_query_name='addresses',)
    city = models.CharField(_('City'), max_length=30)
    street = models.CharField(_('Street'), max_length=50)
    alley = models.CharField(_('Alley'), max_length=30)
    zip_code = models.CharField(_('Zip code'), max_length=40)

    def __str__(self):
        return self.user.first_name


class Shop(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name='shop', related_query_name='shop', )
    name = models.CharField(_('Name'), max_length=150)
    description = models.CharField(_('description'), max_length=150)
    image = models.ImageField(_('Image'), upload_to='users/image')
    slug = models.CharField(_("Slug"), max_length=100)

    def __str__(self):
        return self.name


class Email(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name='emails', related_query_name='emails', )
    # to = models.ForeignKey('self', on_delete=models.DO_NOTHING)
    subject = models.CharField(_("Subject"), max_length=150)
    body = models.TextField(_('body'), )

    def __str__(self):
        return self.user.first_name
