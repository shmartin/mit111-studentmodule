from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Max # Import Max for finding the maximum did
from .models import Document, DocumentDetails, DocumentEvaluation, Program
from users.models import Users

# You might need to import your actual User model if it's in a different app
# from django.contrib.auth import get_user_model
# User = get_user_model()

import os

def submission(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to access the submission page.")
        return redirect('login')
    
    user_instance = Users.objects.get(pk=request.user.pk)
    
    # Fetch programs for the dropdown in the submission form
    programs = Program.objects.all()

    user_evaluations = DocumentEvaluation.objects.filter(dauthor_id=request.user.pk).select_related('did')

    if request.method == 'POST':
        # Get data from the POST request
        dtitle = request.POST.get('dtitle')
        dadviser = request.POST.get('dadviser')
        program_id = request.POST.get('program') # Get the selected program ID
        uploaded_file = request.FILES.get('file_path')

        # --- File Validation ---
        if not uploaded_file:
            messages.error(request, "Please upload a file before submitting.")
            return redirect('submission')

        ext = os.path.splitext(uploaded_file.name)[1].lower()
        allowed_ext = ['.pdf', '.doc', '.docx']
        if ext not in allowed_ext:
            messages.error(request, "Invalid file type. Only PDF, DOC, or DOCX are allowed.")
            return redirect('submission')

        # File size validation (20MB)
        max_size = 20 * 1024 * 1024
        if uploaded_file.size > max_size:
            messages.error(request, "File too large. Maximum size allowed is 20MB.")
            return redirect('submission')
        # --- End File Validation ---

        try:
            # Find the next available 'did'. We find the max existing did and add 1.
            # If no documents exist, start with 1.
            max_did = Document.objects.aggregate(Max('did'))['did__max']
            next_did = (max_did or 0) + 1

            # Get the Program object based on the submitted program_id
            program_instance = Program.objects.get(pid=program_id)

            # Create a new Document instance
            # version is defaulted to 1 in the model
            document_instance = Document.objects.create(
                did=next_did,
                dtitle=dtitle,
                file_path=uploaded_file, # FileField handles saving the file
                version=1 # New submissions are version 1
            )

            # Create a new DocumentDetails instance
            # dauthor is the logged-in user (request.user)
            document_details_instance = DocumentDetails.objects.create(
                did=document_instance, # Link to the newly created Document
                dauthor=user_instance, # Link to the logged-in user
                dadviser=dadviser,
                program=program_instance # Link to the selected Program
            )

            # Note: DocumentEvaluation and DocumentReviewers entries are typically
            # created later in the workflow (e.g., by an admin/chair) when the
            # document is assigned for review or evaluated. They are not created
            # during the initial submission by the student.

            messages.success(request, "Research paper submitted successfully.")
            return redirect('submission')

        except Program.DoesNotExist:
            messages.error(request, "Invalid program selected.")
            return redirect('submission')
        except Exception as e:
            # Catch any other potential errors during creation
            messages.error(request, f"An error occurred during submission: {e}")
            # You might want to log the error for debugging
            # import logging
            # logging.exception("Error during document submission")
            return redirect('submission')


    # Render the page for GET requests or after a failed POST
    context = {
        'doc_eval': user_evaluations, # Pass evaluations filtered for the user
        'programs': programs # Pass all programs for the dropdown
        # 'documents' and 'doc_detail' are not strictly needed in the context
        # based on the template's usage, but you could include them if needed.
        # 'documents': Document.objects.all(),
        # 'doc_detail': DocumentDetails.objects.all(),
    }
    return render(request, 'submission/submission.html', context)

def guidelines(request):
    # You might want to fetch guidelines content from a database or file here
    return render(request, 'submission/guidelines.html')

def help(request):
    # You might want to fetch help content from a database or file here
    return render(request, 'submission/help.html')

# Example view for document detail (based on suggested URL)
# def document_detail(request, did):
#     try:
#         # Fetch the document and related details for the given did (and version 1 for initial submission)
#         document = Document.objects.get(did=did, version=1) # Assuming we show version 1 details
#         details = DocumentDetails.objects.get(did=document) # OneToOneField access
#         evaluations = DocumentEvaluation.objects.filter(did=document).select_related('dauthor')
#         reviewers = DocumentReviewers.objects.filter(did=document, version=1).select_related('reviewer', 'assigned_by') # Assuming we show version 1 reviewers
#
#         context = {
#             'document': document,
#             'details': details,
#             'evaluations': evaluations,
#             'reviewers': reviewers,
#         }
#         return render(request, 'submission/document_detail.html', context) # You'll need to create this template
#     except Document.DoesNotExist:
#         messages.error(request, "Document not found.")
#         return redirect('submission') # Redirect to submission page if document not found
#     except DocumentDetails.DoesNotExist:
#          messages.warning(request, "Document details not found.")
#          # Continue rendering with available info or redirect
#          context = {
#              'document': document,
#              'details': None, # Explicitly None if not found
#              'evaluations': evaluations,
#              'reviewers': reviewers,
#          }
#          return render(request, 'submission/document_detail.html', context)
#     except Exception as e:
#         messages.error(request, f"An error occurred: {e}")
#         return redirect('submission')

# Example view for handling resubmission (based on template action)
# def resubmit_document(request, did):
#     # This view would handle updating an existing document (creating a new version)
#     # and potentially updating DocumentDetails or creating new evaluations/reviews.
#     # This is a more complex workflow and depends on your specific requirements
#     # for handling revisions and versions.
#     pass # Implement resubmission logic here

