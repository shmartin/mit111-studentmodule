from django.db import models

# Create your models here.

class Document(models.Model):
    dtitle = models.CharField(max_length=150)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.dtitle
