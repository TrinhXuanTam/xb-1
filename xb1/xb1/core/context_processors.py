import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from xb1.core.models import Message


def message_processor(request):
    try:
        message = Message.objects.get(pk=1)
        if message.timestamp - datetime.timedelta(minutes=30) < timezone.now() <= message.timestamp:
            return {'message': message.text}
        else:
            return {'message': ""}
    except ObjectDoesNotExist:
        return {'message': ""}
