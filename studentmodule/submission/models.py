from django.db import models
from users.models import User, Program

# Create your models here.

class Document(models.Model):
    dtitle = models.CharField(max_length=150)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.dtitle


class Document_detail(models.Model):
    did = models.ForeignKey(Document, on_delete=models.CASCADE)
    dauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    dadviser = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.did} | {self.author} | {self.dadviser}'

class Document_evaluation(models.Model):
    did = models.ForeignKey(Document, on_delete=models.CASCADE)
    dauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.did} | {self.status}'


# title = foreignkey(docuement.title)
# file_path

# did = foreignkey(document)
# ddid = foreignkey(Document_details)
# deid = foreignkey(document_evaluation)