from django.contrib.messages import get_messages
from django.utils.deprecation import MiddlewareMixin
from api.models import MessageLog

class SaveMessagesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:  # Save messages only for logged-in users
            messages = get_messages(request)
            for message in messages:
                # Save the message to the database
                MessageLog.objects.create(user=request.user, message=str(message))
        return response