from django.contrib import admin
from .models import Document, Document_detail, Document_evaluation

# Register your models here.

admin.site.register(Document)
admin.site.register(Document_detail)
admin.site.register(Document_evaluation)
