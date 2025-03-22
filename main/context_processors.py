from .models import Message

def message_context(request):
    messag = Message.objects.first()
    return {'messag': messag}
