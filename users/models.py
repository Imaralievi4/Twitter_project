import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models, transaction
from django.utils import timezone
from PIL import Image

class MyUserManager(models.Manager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        with transaction.atomic():
            user = self.model(email=email, username=username, **extra_fields) # user = MyUser(email='hhh.mail.ru', password='12323')  user.save()
            user.set_password(password)
            user.generate_activation_code()
            user.save(using=self._db)
            return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=36, blank=True)
    avatar = models.ImageField(upload_to='')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    object = MyUserManager()

    def generate_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    def get_short_name(self):
        return self.first_name

    # def __str__(self):
    #     return f'{self.user.username} Profile'

    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.Image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.Image.path)


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(CustomUser, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

