from django import forms
from .models import Users

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password', min_length=6)

    class Meta:
        model = Users
        fields = ['firstname', 'lastname', 'email'] # Removed 'username'

    # Custom cleaning method for the entire form
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2') # Corrected field name

        # Check if both password fields have data and if they match
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match')

        # Return the cleaned data
        return cleaned_data

    # Optional: Override the save method if you need custom logic
    # For example, to set the password securely using set_password
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     # Hash the password before saving
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
