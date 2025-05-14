from django.urls import path
from . import views # Import views from the current app

urlpatterns = [
    # URL pattern for the main submission page (will be at /submission/)
    path('', views.submission, name='submission'),

    # URL pattern for the guidelines page (will be at /submission/guidelines/)
    path('guidelines/', views.guidelines, name='guidelines'),

    # URL pattern for the help page (will be at /submission/help/)
    path('help/', views.help, name='help'),

    path('documents/<int:document_pk>/', views.document_detail, name='document_detail'),
    

    # Add other URL patterns for your submission app here as needed (e.g., resubmit, download)
    # path('resubmit/<int:document_pk>/', views.resubmit_document, name='resubmit_document'), # will be at /submission/resubmit/5/
    # path('download/<int:document_pk>/', views.download_accepted_paper, name='download_accepted_paper'), # will be at /submission/download/5/
]

    # --- Potential additional URLs based on revue.sql schema ---
    # These are suggestions for URLs you might need to manage the data
    # described in your database schema (Document, DocumentDetails, etc.).
    # You would need to create corresponding view functions for these URLs.

    # Example: URL to view details of a specific document (using the document's primary key)
    # path('document/<int:did>/', views.document_detail, name='document_detail'),

    # Example: URL to handle the submission of a new document (form submission)
    # The main submission page might handle this, but a separate URL could be used if needed.
    # path('submit/', views.submit_document, name='submit_document'),

    # Example: URL to view evaluations for a specific document
    # path('document/<int:did>/evaluations/', views.document_evaluations, name='document_evaluations'),

    # Example: URL to view reviewers assigned to a specific document version
    # path('document/<int:did>/version/<int:version>/reviewers/', views.document_reviewers, name='document_reviewers'),

    # Example: URL for reviewers to submit their evaluation for a document
    # path('review/<int:evaluation_id>/submit/', views.submit_evaluation, name='submit_evaluation'),

    # Example: URL to view a list of all programs
    # path('programs/', views.program_list, name='program_list'),

    # Example: URL to view details of a specific user
    # path('users/<int:uid>/', views.user_detail, name='user_detail'),

