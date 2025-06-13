from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Sermon
from .mixins import SwahiliDateMixin
from django.conf import settings  # Import settings

User = get_user_model()

@receiver(post_save, sender=Sermon)
def send_sermon_notification(sender, instance, created, **kwargs):
    if created:  # Only send email when a new sermon is added
        subject = f"Mahubiri ya leo - {instance.get_swahili_date()}"
        message = f"""
        Habari Mpendwa,

        Unakaribishwa leo kutafakari neno la Mungu:

        Masomo:
        - Somo la Kwanza: {instance.somo_la_kwanza}
        - Somo la Pili: {instance.somo_la_pili}
        - Injili: {instance.injili}

        Bofya link iliyopo chini kusoma tafakari ya leo.: 

        http://mtakatifuambrosi.com/mahubiri/{instance.id}/

        Ubarikiwe!
        """

        # Get all registered user emails
        recipient_list = list(User.objects.values_list('email', flat=True))

        # Send email to all users
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Use the email configured in settings.py
            recipient_list,
            fail_silently=False,
        )
