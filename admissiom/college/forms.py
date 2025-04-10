from django import forms
from django.contrib.auth.models import User
from .models import UploadedDocument, Applicant

class RegisterForm(forms.ModelForm):
    """
    User registration form with password confirmation.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'password',
        }),
        label="Password"
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'confirm_password',
        }),
        label="Confirm Password"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

    def clean(self):
        """
        Validate that password and confirm_password match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError({"confirm_password": "Passwords do not match."})

        return cleaned_data

    def clean_username(self):
        """
        Ensure username is unique.
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """
        Ensure email is unique.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class DocumentUploadForm(forms.ModelForm):
    """
    Form to handle document uploads for applicants.
    """
    applicant = forms.ModelChoiceField(
        queryset=Applicant.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Applicant"
    )
    
    document = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label="Upload Document"
    )

    class Meta:
        model = UploadedDocument
        fields = ['document_type', 'document']  # Add document_type, remove applicant
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_document(self):
        """
        Validate document upload (e.g., file size, type).
        """
        document = self.cleaned_data.get("document")

        if document:
            # Restrict file size to 5MB
            if document.size > 5 * 1024 * 1024:
                raise forms.ValidationError("The document size must be under 5MB.")

            # Restrict file types (example: PDFs and Images)
            allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
            if document.content_type not in allowed_types:
                raise forms.ValidationError("Only PDF, JPG, and PNG files are allowed.")

        return document
