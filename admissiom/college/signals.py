from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Applicant

@receiver(post_save, sender=User)
def create_applicant(sender, instance, created, **kwargs):
    """Create an Applicant only if it doesn't already exist."""
    if created and not hasattr(instance, 'applicant'):
        Applicant.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_applicant(sender, instance, **kwargs):
    """Save the related Applicant only if it exists."""
    if hasattr(instance, 'applicant'):
        instance.applicant.save()