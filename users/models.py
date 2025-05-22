# users/models.py

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission
)
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, user_id, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수입니다.")
        email = self.normalize_email(email)
        user = self.model(user_id=user_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('슈퍼유저는 is_staff=True, is_superuser=True 여야 합니다.')
        return self.create_user(user_id, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    nationality = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 권한 필드 related_name 충돌 방지
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # 기본 user_set 대신
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups')
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # 기본 user_set 대신
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'name', 'birthdate', 'nationality', 'phone']

    def __str__(self):
        return self.user_id
