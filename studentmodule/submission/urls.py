from django.urls import path
from . import views

urlpatterns = [
    path('', views.submission, name='submission'),
    path('submission_history/', views.submission_history, name='submission_history'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('help/', views.help, name='help'),

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
]

