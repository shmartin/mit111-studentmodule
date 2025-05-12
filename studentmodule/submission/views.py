from django.shortcuts import render, redirect
from django.contrib import messages # Import the messages framework
from .models import Document, Document_detail, Document_evaluation
import os

# Create your views here.

def submission(request):

    all_documents = Document.objects.all()
    doc_details = Document_detail.objects.all()
    doc_eval = Document_evaluation.objects.all().select_related('did')

    if request.method == 'POST':
        title = request.POST.get('title')
        abstract = request.POST.get('abstract')
        authors = request.POST.get('authors')
        adviser = request.POST.get('adviser')
        category = request.POST.get('category')
        uploaded_file = request.FILES.get('paper_file')

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            allowed_ext = ['.pdf', '.doc', '.docx']
            if ext not in allowed_ext:
                messages.error(request, "Invalid file type. Only PDF, DOC, or DOCX are allowed.")
                return redirect('submission')

            if uploaded_file.size > 20 * 1024 * 1024:  # 20MB
                messages.error(request, "File too large. Maximum size allowed is 20MB.")
                return redirect('submission')
            
            # Save to Document model (adjust fields as necessary)
            document = Document.objects.create(
                user=request.user,  # adjust if you have a related user field
                file=uploaded_file
            )

            # Save metadata in Document_detail
            Document_detail.objects.create(
                did=document,
                dtitle=title,
                abstract=abstract,
                authors=authors,
                adviser=adviser,
                category=category
            )

            messages.success(request, "Research paper submitted successfully.")
            return redirect('submission')
        else:
            messages.error(request, "Please upload a file before submitting.")
            return redirect('submission')

    context = {}
    context['documents'] = all_documents
    context['doc_detail'] = doc_details
    context['doc_eval'] = doc_eval
    return render(request, 'submission/submission.html', context)

def guidelines(request):
    return render(request, 'submission/guidelines.html', context)

def help(request):
    return render(request, 'submission/help.html')
