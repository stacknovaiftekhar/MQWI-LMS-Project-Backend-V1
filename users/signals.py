import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Teacher, Student


def delete_old_file(instance, field_name):
    """
    Delete old file from storage if a new file is being uploaded.
    """
    try:
        old_file = getattr(instance.__class__.objects.get(pk=instance.pk), field_name)
    except instance.__class__.DoesNotExist:
        return  # New object — no old file yet

    new_file = getattr(instance, field_name)
    if old_file and old_file != new_file and hasattr(old_file, 'path') and os.path.isfile(old_file.path):
        os.remove(old_file.path)


@receiver(pre_save, sender=Teacher)
def delete_old_teacher_image(sender, instance, **kwargs):
    delete_old_file(instance, 'image')


@receiver(pre_save, sender=Student)
def delete_old_student_image(sender, instance, **kwargs):
    delete_old_file(instance, 'image')