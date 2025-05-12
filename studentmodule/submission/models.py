from django.db import models

class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    role = models.CharField(max_length=55)
    firstname = models.CharField(max_length=55)
    lastname = models.CharField(max_length=55)
    email = models.EmailField(max_length=55)
    password = models.CharField(max_length=55) # Consider using Django's built-in authentication

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Program(models.Model):
    pid = models.AutoField(primary_key=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description

# Corresponds to the 'document' table in revue.sql
# PRIMARY KEY (`did`,`version`)
class Document(models.Model):
    did = models.IntegerField() # Corresponds to `did` in SQL
    dtitle = models.CharField(max_length=150) # Corresponds to `dtitle` in SQL
    file_path = models.FileField(upload_to='documents/') # Corresponds to `file_path` in SQL (VARCHAR)
    version = models.IntegerField(default=1) # Corresponds to `version` in SQL

    class Meta:
        unique_together = (('did', 'version'),)

    def __str__(self):
        return f"{self.dtitle} (Version {self.version}, DID: {self.did})"


# Corresponds to the 'document_details' table in revue.sql
# UNIQUE KEY `dauthor` (`dauthor`), UNIQUE KEY `did` (`did`)
# FOREIGN KEY (`did`) REFERENCES `document` (`did`)
# FOREIGN KEY (`dauthor`) REFERENCES `users` (`uid`)
# FOREIGN KEY (`program`) REFERENCES `program` (`pid`)
class DocumentDetails(models.Model):
    did = models.OneToOneField(Document, on_delete=models.CASCADE, primary_key=True) # Corresponds to `did` in SQL, acts as PK
    dauthor = models.OneToOneField(Users, on_delete=models.CASCADE, unique=True) # Corresponds to `dauthor` in SQL
    dadviser = models.CharField(max_length=100) # Corresponds to `dadviser` in SQL
    program = models.ForeignKey(Program, on_delete=models.CASCADE) # Corresponds to `program` in SQL

    def __str__(self):
        # Accessing linked objects for string representation
        return f"Details for {self.did.dtitle} by {self.dauthor.firstname} {self.dauthor.lastname}"


# Corresponds to the 'document_evaluation' table in revue.sql
# PRIMARY KEY (`id`)
# FOREIGN KEY (`did`) REFERENCES `document` (`did`)
# FOREIGN KEY (`dauthor`) REFERENCES `users` (`uid`)
class DocumentEvaluation(models.Model):
    did = models.ForeignKey(Document, on_delete=models.CASCADE) # Corresponds to `did` in SQL
    dauthor = models.ForeignKey(Users, on_delete=models.CASCADE) # Corresponds to `dauthor` in SQL
    feedback = models.CharField(max_length=255) # Corresponds to `feedback` in SQL
    status = models.CharField(max_length=50) # Corresponds to `status` in SQL

    def __str__(self):
        # Accessing linked document title for string representation
        return f"Evaluation Status: {self.status} for {self.did.dtitle}"


# Corresponds to the 'document_reviewers' table in revue.sql
# PRIMARY KEY (`did`,`version`,`reviewer_id`)
# FOREIGN KEY (`assigned_by`) REFERENCES `users` (`uid`)
# FOREIGN KEY (`did`,`version`) REFERENCES `document` (`did`, `version`)
# FOREIGN KEY (`reviewer_id`) REFERENCES `users` (`uid`)
class DocumentReviewers(models.Model):
    did = models.ForeignKey(Document, on_delete=models.CASCADE) # Links to the Document object
    version = models.IntegerField() # Corresponds to `version` in SQL, part of composite PK
    # 'reviewer_id' is a FK to users(uid), part of composite PK. References the Users model.
    reviewer = models.ForeignKey(Users, on_delete=models.CASCADE) # Corresponds to `reviewer_id` in SQL
    review_status = models.CharField(max_length=50) # Corresponds to `review_status` in SQL
    review_date = models.DateTimeField(null=True, blank=True) # Corresponds to `review_date` in SQL (can be null initially)
    assigned_date = models.DateTimeField() # Corresponds to `assigned_date` in SQL
    # 'assigned_by' is a FK to users(uid). References the Users model.
    assigned_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='assigned_reviews') # Corresponds to `assigned_by` in SQL

    class Meta:
        # Enforce the composite primary key constraint from SQL
        unique_together = (('did', 'version', 'reviewer'),)
    
    def __str__(self):
        # Accessing linked objects for string representation
        return f"Review of {self.did.dtitle} (v{self.version}) by {self.reviewer.firstname} {self.reviewer.lastname}"

# The 'program' and 'users' tables from SQL would correspond to Django models
# that you should have defined elsewhere in your project (e.g., in a 'users' app).
# The placeholder models above are just for context if you don't have them yet.

