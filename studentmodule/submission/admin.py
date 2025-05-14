from django.contrib import admin
from .models import Document, DocumentDetails, DocumentEvaluation, DocumentReviewers, DocumentSubmissionLog, Program

admin.site.register(Document)
admin.site.register(DocumentDetails)
admin.site.register(DocumentEvaluation)
admin.site.register(DocumentReviewers)
admin.site.register(DocumentSubmissionLog)
admin.site.register(Program)
