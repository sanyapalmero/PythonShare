from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.db import models

#Custom user model

class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        user = self.model(username = username,**kwargs)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username = username,
            role = User.ROLE_ADMIN
            )
        user.set_password(password)
        user.save(using = self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ADMIN, "Admin"),
    ]

    username = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=64,choices=ROLE_CHOICES, default=ROLE_USER)

    @property
    def is_superuser(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_ADMIN

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_perms(self, perm_list, obj=None):
        return self.is_staff

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username