import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .forms import RegisterForm, DocumentUploadForm
from .models import UploadedDocument, Applicant, Payment, AdmissionStatus

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("college:register")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Ensure the user has only one Applicant profile
        applicant, created = Applicant.objects.get_or_create(user=user)

        messages.success(request, "Registration successful!")
        return redirect("college:login")

    return render(request, "register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect('college:dashboard')
        
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return redirect("college:login")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("college:dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")

@login_required
def dashboard(request):
    # Get or create applicant profile
    applicant, created = Applicant.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "Welcome! Please complete your profile.")
        return redirect("college:register")
    
    return render(request, 'college/dashboard.html', {
        'applicant': applicant,
        'documents_complete': applicant.submitted_documents
    })

@login_required
def upload_document(request):
    applicant, _ = Applicant.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.applicant = applicant
            doc.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect('college:upload_document')
        else:
            messages.error(request, "Invalid form. Please check your upload.")
    else:
        form = DocumentUploadForm()

    documents = UploadedDocument.objects.filter(applicant=applicant).order_by('-uploaded_at')
    return render(request, 'college/upload_document.html', {
        'form': form,
        'uploaded_documents': documents,
        'applicant': applicant,
    })
@login_required
def delete_document(request, id):
    try:
        document = get_object_or_404(UploadedDocument, id=id, applicant=request.user.applicant)
        if document.document:
            file_path = os.path.join(settings.MEDIA_ROOT, document.document.name)
            if os.path.exists(file_path):
                os.remove(file_path)
        document.delete()
        messages.success(request, "Document deleted.")
    except Exception as e:
        messages.error(request, f"Deletion failed: {str(e)}")
    
    return redirect("college:upload_document")

@login_required
def payment_page(request):
    applicant = get_object_or_404(Applicant, user=request.user)
    
    if not applicant.submitted_documents:
        messages.error(request, "Please upload all required documents first.")
        return redirect("college:upload_document")

    if request.method == "POST":
        try:
            selected_year = request.POST.get("year")
            if not selected_year:
                raise ValueError("Please select a year")
            
            request.session["payment_data"] = {
                "year": selected_year,
                "amount": 55000  # Fixed amount
            }
            return redirect("college:complete_payment")
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, "college/payment_page.html")

@login_required
def complete_payment(request):
    applicant = get_object_or_404(Applicant, user=request.user)
    payment_data = request.session.get("payment_data")
    
    if not payment_data:
        messages.error(request, "Please select payment options first.")
        return redirect("college:payment_page")

    if request.method == "POST":
        try:
            payment_method = request.POST.get("payment_method", "").strip()
            card_number = request.POST.get("card_number", "").strip()
            upi_id = request.POST.get("upi_id", "").strip()

            if not payment_method:
                raise ValueError("Payment method required")

            if payment_method == "Card" and not card_number:
                raise ValueError("Card number required")
            elif payment_method == "UPI" and not upi_id:
                raise ValueError("UPI ID required")

            Payment.objects.create(
                applicant=applicant,
                amount=payment_data["amount"],
                payment_method=payment_method,
                transaction_id=f"TXN{get_random_string(10).upper()}",
                status="Completed",
                created_at=timezone.now(),
            )

            admission_status, _ = AdmissionStatus.objects.get_or_create(applicant=applicant)
            admission_status.fees_paid = True
            admission_status.save()

            del request.session["payment_data"]
            messages.success(request, f"Payment of ₹{payment_data['amount']} successful!")
            return redirect("college:dashboard")
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, "college/complete_payment.html", {
        "year": payment_data["year"],
        "amount": payment_data["amount"]
    })

@login_required
def admission_status(request):
    applicant = get_object_or_404(Applicant, user=request.user)
    status, _ = AdmissionStatus.objects.get_or_create(applicant=applicant)
    return render(request, 'college/admission_status.html', {
        'applicant': applicant,
        'status': status
    })

def payment_success(request):
    return render(request, 'college/payment_success.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home") 