<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib import messages

=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.conf import settings
import os

from .forms import RegisterForm
from .models import UploadedDocument
>>>>>>> 69002000 (made changes)

def home(request):
    return render(request, 'home.html')

<<<<<<< HEAD

=======
>>>>>>> 69002000 (made changes)
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
<<<<<<< HEAD
            login(request, user)  # Auto-login after registration
            messages.success(request, "Registration successful. Welcome!")
            return redirect("http://127.0.0.1:8000/college/dashboard/")  # Corrected redirect
=======
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect(reverse("dashboard"))
>>>>>>> 69002000 (made changes)
    else:
        form = RegisterForm()
    
    return render(request, "register.html", {"form": form})

<<<<<<< HEAD

def login_view(request):
    if request.method == "POST":  # Simplified condition
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        next_url = request.GET.get("next", "dashboard")  # Default redirect to dashboard
=======
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        next_url = request.GET.get("next", ("http://127.0.0.1:8000/college/dashboard/"))
>>>>>>> 69002000 (made changes)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
<<<<<<< HEAD
            return redirect("http://127.0.0.1:8000/college/dashboard/")  # Redirect to intended page or dashboard
=======
            return redirect("http://127.0.0.1:8000/college/dashboard/")
>>>>>>> 69002000 (made changes)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

<<<<<<< HEAD

=======
>>>>>>> 69002000 (made changes)
@login_required
def dashboard(request):
    return render(request, 'college/dashboard.html')

<<<<<<< HEAD

def logout_view(request):
    logout(request)
    return redirect("http://127.0.0.1:8000/college/")  # Redirect to login after logout
=======
@login_required
def upload_document(request):
    if request.method == 'POST' and request.FILES.get('document'):
        document_type = request.POST.get('document_type')
        uploaded_file = request.FILES['document']

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(uploaded_file.name, uploaded_file)

        UploadedDocument.objects.create(
            document_type=document_type,
            document=uploaded_file
        )

        messages.success(request, 'Document uploaded successfully!')
        return redirect("http://127.0.0.1:8000/college/upload_document/")

    uploaded_documents = UploadedDocument.objects.all()
    uploaded_types = [doc.document_type for doc in uploaded_documents]
    available_document_types = ['Aadhar Card', 'PAN Card', 'Passport', 'Driving License', 'Marksheet']
    remaining_document_types = [doc for doc in available_document_types if doc not in uploaded_types]

    return render(request, 'college/upload_document.html', {
        'uploaded_documents': uploaded_documents,
        'available_document_types': remaining_document_types
    })

@login_required
def delete_document(request, id):
    document = get_object_or_404(UploadedDocument, id=id)
    document.delete()
    messages.success(request, 'Document deleted successfully!')
    return redirect("http://127.0.0.1:8000/college/upload_document/")

@login_required
def complete_payment(request):
    """
    User selects payment method and enters payment details.
    """
    selected_year = request.session.get("selected_year", "")
    amount = request.session.get("amount", 0)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        card_number = request.POST.get("card_number", "").strip()
        upi_id = request.POST.get("upi_id", "").strip()

        # Basic validation
        if payment_method == "card" and not card_number:
            messages.error(request, "Please enter a valid card number.")
        elif payment_method == "upi" and not upi_id:
            messages.error(request, "Please enter a valid UPI ID.")
        else:
            messages.success(request, f"Payment of ₹{amount} for {selected_year} year successful!")
            return redirect("college:dashboard")  # Redirect to dashboard after payment

    return render(request, "college/complete_payment.html", {
        "selected_year": selected_year,
        "amount": amount
    })


@login_required
def payment_page(request):
    if request.method == "POST":
        selected_year = request.POST.get("year")
        amount = 55000  # Fixed fee for each year
        messages.success(request, f"Payment of ₹{amount} for {selected_year} year successful!")
        return redirect("college:dashboard")  # Redirect to dashboard after payment

    return render(request, "college/payment_page.html")


@login_required
def admission_status(request):
    # Dummy data (Replace with database queries)
    admission_status = "Accepted"  # or "Rejected" based on actual status
    fees_paid = True  # Change based on actual payment record
    documents_completed = True  # Check if all required documents are uploaded
    admission_approved = fees_paid and documents_completed and admission_status == "Accepted"

    return render(request, 'college/admission_status.html', {
        'admission_status': admission_status,
        'fees_paid': fees_paid,
        'documents_completed': documents_completed,
        'admission_approved': admission_approved
    })


def logout_view(request):
    logout(request)
    return redirect(reverse("home"))
>>>>>>> 69002000 (made changes)
