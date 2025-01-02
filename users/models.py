from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, full_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255 , blank=True, null=True)
    adress = models.CharField(max_length=255 , blank=True, null=True)
    number = models.CharField(max_length=255 , blank=True, null=True)
    company_tr = models.CharField(max_length=255 ,blank=True, null=True)
    tax_number = models.CharField(max_length=50, unique=True, blank=True, null=True)  # New tax number field
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Image field for profile image

    # Add related_name to avoid conflict with auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # custom related name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
