from django.shortcuts import render
from .models import Document, Document_detail, Document_evaluation

# Create your views here.

def submission(request):

    all_documents = Document.objects.all()
    doc_details = Document_detail.objects.all()
    doc_eval = Document_evaluation.objects.all().select_related('did')

    if request.method == 'POST':
        pass

    context = {}
    context['documents'] = all_documents
    context['doc_detail'] = doc_details
    context['doc_eval'] = doc_eval
    return render(request, 'submission/submission.html', context)