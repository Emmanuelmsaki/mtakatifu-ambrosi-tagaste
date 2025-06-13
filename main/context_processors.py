from .models import Message
from django.conf import settings

def message_context(request):
    messag = Message.objects.first()
    return {'messag': messag,
            'email_user': settings.EMAIL_HOST_USER,
            }
