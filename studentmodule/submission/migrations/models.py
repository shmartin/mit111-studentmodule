from django.db import models
from django.conf import settings # Import settings to reference AUTH_USER_MODEL


class Program(models.Model):
    pid = models.AutoField(primary_key=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description


# Corresponds to the 'document' table in revue.sql
# PRIMARY KEY (did,version)
class Document(models.Model):
    did = models.IntegerField() # Corresponds to did in SQL
    dtitle = models.CharField(max_length=150) # Corresponds to dtitle in SQL
    file_path = models.FileField(upload_to='documents/') # Corresponds to file_path in SQL (VARCHAR)
    version = models.IntegerField(default=1) # Corresponds to version in SQL

    class Meta:
        unique_together = (('did', 'version'),)

    def __str__(self):
        return f"{self.dtitle} (Version {self.version}, DID: {self.did})"


# Corresponds to the 'document_details' table in revue.sql
# UNIQUE KEY dauthor (dauthor), UNIQUE KEY did (did)
# FOREIGN KEY (did) REFERENCES document (did)
# FOREIGN KEY (dauthor) REFERENCES users (uid)
# FOREIGN KEY (program) REFERENCES program (pid)
class DocumentDetails(models.Model):
    did = models.OneToOneField(Document, on_delete=models.CASCADE, primary_key=True) # Corresponds to did in SQL, acts as PK
    # --- CORRECT WAY TO REFERENCE AUTH_USER_MODEL IN ForeignKey/OneToOneField ---
    # Use the string 'appname.ModelName' from settings.AUTH_USER_MODEL
    dauthor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Corresponds to dauthor in SQL
    # --- End Correction ---
    dadviser = models.CharField(max_length=100) # Corresponds to dadviser in SQL
    program = models.ForeignKey(Program, on_delete=models.CASCADE) # Corresponds to program in SQL

    def __str__(self):
        # Access related user fields normally
        return f"Details for {self.did.dtitle} by {self.dauthor.firstname} {self.dauthor.lastname}"


# Corresponds to the 'document_evaluation' table in revue.sql
# PRIMARY KEY (id)
# FOREIGN KEY (did) REFERENCES document (did)
# FOREIGN KEY (dauthor) REFERENCES users (uid)
class DocumentEvaluation(models.Model):
    did = models.ForeignKey(Document, on_delete=models.CASCADE) # Corresponds to did in SQL
    # --- CORRECT WAY TO REFERENCE AUTH_USER_MODEL ---
    dauthor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Corresponds to dauthor in SQL
    # --- End Correction ---
    feedback = models.CharField(max_length=255) # Corresponds to feedback in SQL
    status = models.CharField(max_length=50) # Corresponds to status in SQL

    def __str__(self):
        # Access related user fields normally
        return f"Evaluation Status: {self.status} for {self.did.dtitle}"


# Corresponds to the 'document_reviewers' table in revue.sql
# PRIMARY KEY (did,version,reviewer_id)
# FOREIGN KEY (assigned_by) REFERENCES users (uid)
# FOREIGN KEY (did,version) REFERENCES document (did, version)
# FOREIGN KEY (reviewer_id) REFERENCES users (uid)
class DocumentReviewers(models.Model):
    did = models.ForeignKey(Document, on_delete=models.CASCADE) # Links to the Document object
    version = models.IntegerField() # Corresponds to version in SQL, part of composite PK
    # --- CORRECT WAY TO REFERENCE AUTH_USER_MODEL ---
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Corresponds to reviewer_id in SQL
    # --- End Correction ---
    review_status = models.CharField(max_length=50) # Corresponds to review_status in SQL
    review_date = models.DateTimeField(null=True, blank=True) # Corresponds to review_date in SQL (can be null initially)
    assigned_date = models.DateTimeField() # Corresponds to assigned_date in SQL
    # --- CORRECT WAY TO REFERENCE AUTH_USER_MODEL ---
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_reviews') # Corresponds to assigned_by in SQL
    # --- End Correction ---

    class Meta:
        unique_together = (('did', 'version', 'reviewer'),)

    def __str__(self):
        # Access related user fields normally
        return f"Review of {self.did.dtitle} (v{self.version}) by {self.reviewer.firstname} {self.reviewer.lastname}"


# Corresponds to the new 'document_submission_log' table
class DocumentSubmissionLog(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    # --- CORRECT WAY TO REFERENCE AUTH_USER_MODEL ---
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # --- End Correction ---
    submission_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['document', 'submission_timestamp']

    def __str__(self):
        # Access related user fields normally
        return f"Submission of {self.document.dtitle} (v{self.document.version}) by {self.submitted_by.firstname} on {self.submission_timestamp.strftime('%Y-%m-%d %H:%M')}"

