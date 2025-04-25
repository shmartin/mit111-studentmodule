from django.shortcuts import render
from .models import Document

# Create your views here.

def submission(request):
    all_documents = Document.objects.all()
    return render(request, 'submission/submission.html', {'documents': all_documents})