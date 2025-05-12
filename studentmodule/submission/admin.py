from django.contrib import admin
from .models import Document, DocumentDetails, DocumentEvaluation, DocumentReviewers, Program, Users

# Register your models here with the Django admin site.
# This makes them available in the Django administration interface
# for easy management and viewing of data.


admin.site.register(Document)
admin.site.register(DocumentDetails)
admin.site.register(DocumentEvaluation)
admin.site.register(DocumentReviewers)
admin.site.register(Program)
admin.site.register(Users)
