from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator
import os
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from django.core.files.storage import FileSystemStorage
from .utils import get_upload_path

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Delete existing file if it exists
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name
def upload_document_path(instance, filename):
    """Generate organized upload path: documents/username/year/month/doc_type/filename"""
    ext = filename.split('.')[-1]
    filename = f"{instance.document_type.replace(' ', '_')}_{instance.applicant.user.username}.{ext}"
    return os.path.join(
        "documents",
        instance.applicant.user.username,
        timezone.now().strftime("%Y/%m"),
        filename
    )
class Applicant(models.Model):
    APPLICATION_STATUS = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"), 
        ("Rejected", "Rejected"),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="applicant"
    )
    applied_course = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        verbose_name="Applied Course"
    )
    application_status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS,
        default="Pending",
        verbose_name="Application Status"
    )
    submitted_documents = models.BooleanField(
        default=False,
        verbose_name="Documents Submitted"
    )
    applied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Application Date"
    )

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.applied_course or 'No Course'}"

class UploadedDocument(models.Model):
    DOCUMENT_TYPES = [
        ('Aadhaar Card', 'Aadhaar Card'),
        ('PAN Card', 'PAN Card'),
        ('10th Marksheet', '10th Marksheet'),
        ('12th Marksheet', '12th Marksheet'),
        ('Degree Certificate', 'Degree Certificate'),
    ]

    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE, related_name='uploaded_documents')
    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPES)
    document = models.FileField(
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.user.username} - {self.document_type}"

    def save(self, *args, **kwargs):
        """Auto-populate file metadata before saving"""
        if self.document and not self.pk:
            self.file_size = self.document.size
            self.file_type = self.document.name.split('.')[-1].upper()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Clean up files when document is deleted"""
        if self.document:
            storage = self.document.storage
            if storage.exists(self.document.name):
                storage.delete(self.document.name)
        super().delete(*args, **kwargs)

    @property
    def file_url(self):
        """Safe URL accessor"""
        return self.document.url if self.document else None

    @property
    def human_readable_size(self):
        """Convert bytes to human-readable format"""
        if not self.file_size:
            return "0 bytes"
        for unit in ['bytes', 'KB', 'MB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} GB"
    
class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        ONLINE = 'ON', _('Online')
        CASH = 'CA', _('Cash')
        CARD = 'CD', _('Card')
        UPI = 'UP', _('UPI')
        BANK_TRANSFER = 'BT', _('Bank Transfer')
        WALLET = 'WL', _('Digital Wallet')

    class PaymentStatus(models.TextChoices):
        PENDING = 'PE', _('Pending')
        COMPLETED = 'CO', _('Completed')
        FAILED = 'FA', _('Failed')
        REFUNDED = 'RE', _('Refunded')
        PARTIALLY_REFUNDED = 'PR', _('Partially Refunded')
        CANCELLED = 'CA', _('Cancelled')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('Payment ID')
    )
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_('Applicant')
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name=_('Amount')
    )
    currency = models.CharField(
        max_length=3,
        default='INR',
        verbose_name=_('Currency')
    )
    payment_method = models.CharField(
        max_length=2,
        choices=PaymentMethod.choices,
        verbose_name=_('Payment Method')
    )
    transaction_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_('Transaction ID')
    )
    status = models.CharField(
        max_length=2,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name=_('Status')
    )
    payment_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Payment Date')
    )
    processed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Processed Date')
    )
    receipt = models.FileField(
        upload_to='payment_receipts/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])
        ],
        null=True,
        blank=True,
        verbose_name=_('Receipt')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Internal Notes')
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP Address')
    )
    invoice_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('Invoice Number')
    )

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['status', 'payment_date']),
            models.Index(fields=['applicant', 'payment_date']),
        ]

    def __str__(self):
        return f"{self.invoice_number or 'INV-N/A'} - {self.applicant} ({self.get_amount_display()})"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        if self.status == self.PaymentStatus.COMPLETED and not self.processed_date:
            self.processed_date = timezone.now()
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        return f"INV-{self.payment_date.strftime('%Y%m%d')}-{str(self.id)[:8].upper()}"

    def get_amount_display(self):
        return f"{self.currency} {self.amount:,.2f}"

    @property
    def is_successful(self):
        return self.status in [self.PaymentStatus.COMPLETED, self.PaymentStatus.REFUNDED]

    @property
    def receipt_url(self):
        return self.receipt.url if self.receipt else None

class AdmissionStatus(models.Model):
    applicant = models.OneToOneField(
        Applicant,
        on_delete=models.CASCADE,
        related_name="status",
        verbose_name="Applicant"
    )
    fees_paid = models.BooleanField(default=False, verbose_name="Fees Paid")
    documents_completed = models.BooleanField(default=False, verbose_name="Documents Completed")
    admission_approved = models.BooleanField(default=False, verbose_name="Admission Approved")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Admission Status"
        verbose_name_plural = "Admission Statuses"

    def save(self, *args, **kwargs):
        self.admission_approved = self.fees_paid and self.documents_completed and self.applicant.application_status == "Accepted"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.applicant.user.username} - {'Approved' if self.admission_approved else 'Pending'}"
