from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, phone, password):
        """
        Creates and saves an user with email, name, lastname y phone and password.
        """
        if not email or not first_name or not last_name or not phone or not password:
            raise ValueError('Users must have an email address, a first name, a last name, a phone and a password.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, password):
        """
        Creates and saves a superuser with email, name, lastname y phone and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            phone,
            password
        )
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Client(PermissionsMixin, AbstractBaseUser):
    """
       Client common information.
       """
    phone_regex = RegexValidator(regex=r'^\+?\(?\d{0,5}\)?[\-\.\s]?([0-9]*[\-\.\s]?)*\d*$')

    email = models.EmailField(verbose_name='Email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True,
                             help_text='por ej: 03543-440903, 3516618348')

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True, help_text='The User data is correct.')
    is_admin = models.BooleanField(default=False, help_text='The User has admin privileges.')
    is_staff = models.BooleanField(default=False, help_text='The user can log into this admin site.')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)


class CurrentAccount(models.Model):
    """
    Current account information.
    """
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='accounts')

    def __str__(self):
        return "{}" .format(self.client)


class Movement(models.Model):
    """
    Movement information.
    """
    account = models.ForeignKey(CurrentAccount, on_delete=models.PROTECT, related_name='movements')
    amount = models.IntegerField()
    description = models.CharField(max_length=125)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}" .format(self.account, self.amount)
