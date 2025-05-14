from django.shortcuts import render, redirect, get_object_or_404 # Import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Max, OuterRef, Subquery
from .models import Document, DocumentDetails, DocumentEvaluation, Program, DocumentSubmissionLog, DocumentReviewers # Make sure DocumentReviewers is imported
from users.models import Users  # Make sure Users model is imported
from django.utils import timezone # Import timezone for working with datetimes

import os # Import os for file path operations
import traceback # Import traceback module for debugging

# The submission view handles displaying the submission page,
def submission(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to access the submission page.")
        return redirect('login') # Assuming 'login' is the URL name for the login page

    # Explicitly fetch the user instance from the database.
    try:
        user_instance = Users.objects.get(pk=request.user.pk)
    except Users.DoesNotExist:
        messages.error(request, "User not found in database. Please log in again.")
        logout(request)
        return redirect('login')
    except Exception as e:
        messages.error(request, f"Error fetching user details: {e}")
        # Log the exception details...
        logout(request)
        return redirect('login')


    # Fetch all available programs.
    programs = Program.objects.all()

    # Fetch document evaluations related to the current logged-in user as the author.
    doc_eval_notifications = DocumentEvaluation.objects.filter(dauthor__pk=user_instance.pk).select_related('did')


    # --- Logic for "My Latest Submissions" Table ---
    submitted_document_pks = DocumentDetails.objects.filter(dauthor__pk=user_instance.pk).values_list('did__pk', flat=True)

    latest_versions_subquery = Document.objects.filter(
        did=OuterRef('did')
    ).order_by('-version').values('version')[:1]

    latest_documents = Document.objects.filter(
        pk__in=submitted_document_pks,
        version=Subquery(latest_versions_subquery)
    ).select_related('documentdetails')

    user_latest_submissions_data = []
    for document in latest_documents:
        evaluation = DocumentEvaluation.objects.filter(did__did=document.did).order_by('-id').first()

        status = "Submitted" # Default status if no evaluation is found
        if evaluation:
            status = evaluation.status # Get status from evaluation if it exists

    
        # Initialize action_text to an empty string by default
        action_text = ""

        if status == 'Under Review':
            action_text = "View"
        elif status == 'Revision Required':
            action_text = "Resubmit"
        elif status == 'Accepted':
            action_text = "OK"
    

        submission_log_entry = DocumentSubmissionLog.objects.filter(
            document=document
        ).order_by('-submission_timestamp').first()

        submitted_at = submission_log_entry.submission_timestamp if submission_log_entry else None

        user_latest_submissions_data.append({
            'document_obj': document,
            'title': document.dtitle,
            'status': status,          # Pass the determined status
            'action_text': action_text, # Pass the determined action text
            'version': document.version,
            'submitted_at': submitted_at,
        })


    # --- Logic for "Submission History" Table (All Versions) ---
    all_user_documents = Document.objects.filter(
        documentdetails__dauthor__pk=user_instance.pk # Use the reverse relation and filter by user's PK
    ).order_by('did', 'version')

    user_history_data = []
    for document in all_user_documents:
        evaluation = DocumentEvaluation.objects.filter(did__did=document.did).order_by('-id').first()

        status = "Submitted"
        if evaluation:
            status = evaluation.status

        action_text = "View"
        if status == 'Accepted':
             action_text = "OK"

        submission_log_entry = DocumentSubmissionLog.objects.filter(
            document=document
        ).order_by('-submission_timestamp').first()

        submitted_at = submission_log_entry.submission_timestamp if submission_log_entry else None


        user_history_data.append({
            'document_obj': document,
            'title': document.dtitle,
            'version': document.version,
            'status': status,
            'action_text': action_text,
            'submitted_at': submitted_at,
        })
    

    # --- Logic for Handling POST Requests (New Submission) ---
    if request.method == 'POST':
        dtitle = request.POST.get('dtitle')
        dadviser = request.POST.get('dadviser')
        program_name = request.POST.get('program')
        uploaded_file = request.FILES.get('file_path') # Get the uploaded file

    
        if not uploaded_file:
            messages.error(request, "Please upload a file before submitting.")
            return redirect('submission')

        ext = os.path.splitext(uploaded_file.name)[1].lower()
        allowed_ext = ['.pdf', '.doc', '.docx']
        if ext not in allowed_ext:
            messages.error(request, "Invalid file type. Only PDF, DOC, or DOCX are allowed.")
            return redirect('submission')

        max_size = 20 * 1024 * 1024
        if uploaded_file.size > max_size:
            messages.error(request, "File too large. Maximum size allowed is 20MB.")
            return redirect('submission')
        

        # --- Database Creation ---
        try:
            # Find the next available 'did'.
            max_did = Document.objects.aggregate(Max('did'))['did__max']
            next_did = (max_did or 0) + 1

            # Get or create the Program object.
            program_instance, created = Program.objects.get_or_create(
                description__iexact=program_name,
                defaults={'description': program_name}
            )

            # Create a new Document instance for the initial submission (version 1).
            document_instance = Document.objects.create(
                did=next_did,
                dtitle=dtitle,
                file_path=uploaded_file,
                version=1
            )

            # Explicitly fetch the user instance for the assignment *within this block*.
            try:
                correct_user_instance_for_assignment = Users.objects.get(pk=request.user.pk)
            except Users.DoesNotExist:
                 messages.error(request, "Authenticated user not found in database during assignment process.")
                 return redirect('submission')

           
            # Create a new DocumentDetails instance, linking it to the new Document and the user.
            document_details_instance = DocumentDetails.objects.create(
                did=document_instance, # Link to the newly created Document (OneToOneField)
                dauthor=correct_user_instance_for_assignment, # <<< Use the re-fetched instance here
                dadviser=dadviser,
                program=program_instance # Link to the Program object
            )

            # Create a log entry in the new DocumentSubmissionLog table.
            DocumentSubmissionLog.objects.create(
                document=document_instance,
                submitted_by=correct_user_instance_for_assignment, # <<< Use the re-fetched instance here too
            )


            # Add a success message and redirect back to the submission page.
            messages.success(request, "Research paper submitted successfully.")
            return redirect('submission')

        except Exception as e:
            messages.error(request, f"An error occurred during submission: {e}")
            return redirect('submission') # Redirect back to the submission page


    # --- Render the Page (for GET requests or after failed POST) ---
    context = {
        'doc_eval': doc_eval_notifications, # Data for the notification section
        'programs': programs, # Data for the program dropdown (optional if using text input)
        'latest_submissions': user_latest_submissions_data, # Data for the "My Latest Submissions" table
        'submission_history': user_history_data, # Data for the "Submission History" table
    }
    return render(request, 'submission/submission.html', context)


# --- Other Views (Guidelines, Help) ---
# These views are simple and just render static templates.

def guidelines(request):
    # Renders the guidelines page.
    return render(request, 'submission/guidelines.html')

def help(request):
    # Renders the help page.
    return render(request, 'submission/help.html')


# --- ADDED VIEW FUNCTION FOR DOCUMENT DETAIL ---
# This function will handle requests to display details for a specific document.
def document_detail(request, document_pk):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to view document details.")
        return redirect('login')

    # Use get_object_or_404 to retrieve the Document object by its primary key (pk)
    # If a document with the given pk doesn't exist, it will raise a 404 error
    document = get_object_or_404(Document, pk=document_pk)

    # Fetch related DocumentDetails for this document
    # Use .first() as did is a OneToOneField acting as PK in DocumentDetails
    details = DocumentDetails.objects.filter(did=document).first()

    # Fetch the latest evaluation for this document's DID
    # Note: DocumentEvaluation is linked to Document by 'did' field, not (did, version)
    latest_evaluation = DocumentEvaluation.objects.filter(did__did=document.did).order_by('-id').first()

    # Fetch the latest submission log entry for this specific document version
    latest_submission_log = DocumentSubmissionLog.objects.filter(document=document).order_by('-submission_timestamp').first()

    # --- ADDED: Fetch DocumentReviewers for this document and version ---
    # Assuming DocumentReviewers links to Document by did and version
    reviewers = DocumentReviewers.objects.filter(
        did=document,      # Filter by the Document object (matches did and version)
        version=document.version # Ensure it's for the current version being viewed
    ).select_related('reviewer') # Select related User object to access reviewer details efficiently
    

    # Prepare context data to pass to the template
    context = {
        'document': document,
        'details': details, # Pass details if fetched
        'latest_evaluation': latest_evaluation, # Pass latest evaluation
        'latest_submission_log': latest_submission_log, # Pass latest submission log
        'reviewers': reviewers, # --- ADDED: Pass the fetched reviewers ---
    }

    # Render a template to display the document details
    # Ensure you have created 'submission/document_detail.html'
    return render(request, 'submission/document_detail.html', context)










