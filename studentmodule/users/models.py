from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Create your models here.

# Custom Manager for the Users model
# This manager is required when using AbstractBaseUser
class UsersManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        # Normalize the email address by lowercasing the domain part
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # Set the password securely
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        # Ensure required superuser fields are set
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Superusers should be active

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Create the superuser using the create_user method
        return self.create_user(email, password, **extra_fields)


# Corresponds to the 'users' table in revue.sql
# Inherit from AbstractBaseUser and PermissionsMixin for Django authentication compatibility
class Users(AbstractBaseUser, PermissionsMixin):
    role = models.CharField(max_length=55)
    firstname = models.CharField(max_length=55)
    lastname = models.CharField(max_length=55)
    email = models.EmailField(max_length=255, unique=True) # Email should be unique
    is_active = models.BooleanField(default=True) # Can the user log in?
    is_staff = models.BooleanField(default=False) # Can the user access the admin site?
    # is_superuser is provided by PermissionsMixin

    # Fields for tracking login dates (optional but standard)
    # last_login = models.DateTimeField(null=True, blank=True) # Provided by AbstractBaseUser
    # date_joined = models.DateTimeField(auto_now_add=True) # Provided by AbstractBaseUser

    # Define the field used as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['firstname', 'lastname', 'role'] # Include other required fields

    # Link the custom manager to the model
    objects = UsersManager()

    def __str__(self):
        # Display the full name and role for easy identification
        return f'{self.firstname} {self.lastname} ({self.role})'

    # Required methods for AbstractBaseUser (often handled by manager or default implementation)
    # def get_full_name(self):
    #     return f"{self.firstname} {self.lastname}"
    #
    # def get_short_name(self):
    #     return self.firstname

    # PermissionsMixin provides methods like has_perm, has_module_perms, groups, user_permissions


# Corresponds to the 'program' table in revue.sql
class Program(models.Model):
    # pid is the primary key in the SQL schema
    pid = models.AutoField(primary_key=True)
    # description is a field in the SQL schema
    description = models.CharField(max_length=150)

    def __str__(self):
        # Display the program description
        return self.description


