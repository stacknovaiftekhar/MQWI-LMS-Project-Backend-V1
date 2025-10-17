from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from enrolls.models import Enrollment

@receiver(post_save, sender=Payment)
def mark_enrollment_as_enrolled(sender, instance, **kwargs):
    if instance.status == 'Verified':
        try:
            enrollment = instance.enrollment
            if enrollment.status != 'Enrolled':
                enrollment.status = 'Enrolled'
                enrollment.save()
        except Enrollment.DoesNotExist:
            pass  # Enrollment not found – silently skip or handle if needed