from django.db import models

# Create your models here.

class User(models.Model):
    firstname = models.CharField(max_length=55)
    lastname = models.CharField(max_length=55)
    email = models.EmailField(max_length=55)
    password = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class Program(models.Model):
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description