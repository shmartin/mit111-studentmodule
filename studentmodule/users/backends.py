from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q # Import Q object for complex lookups

# Get your custom User model
Users = get_user_model()

class EmailBackend(BaseBackend):
    """
    Custom authentication backend that authenticates users by email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates a user based on email and password.

        Args:
            request: The current request.
            username: The value entered in the username field (which is email in our case).
            password: The password entered by the user.
            **kwargs: Additional keyword arguments.

        Returns:
            The authenticated user object if credentials are valid, None otherwise.
        """
        try:
            # Attempt to find the user by their email address (case-insensitive lookup)
            # Use Q object for case-insensitive email lookup across different databases
            user = Users.objects.get(Q(email__iexact=username))
        except Users.DoesNotExist:
            # No user found with the given email
            return None

        # Check if the provided password is correct for the found user
        # user.check_password() handles the hashing comparison
        if user.check_password(password):
            # Return the user object if authentication is successful
            return user
        else:
            # Password does not match
            return None

    def get_user(self, user_id):
        """
        Required by Django's authentication system to retrieve a user by their primary key.
        """
        try:
            # Retrieve the user by their primary key (Django's internal 'id')
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            # User not found
            return None

