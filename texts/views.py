from django.contrib.auth.models import User
from django.http import HttpResponse
from twilio.rest import Client
import os
from django.views.decorators.csrf import csrf_exempt


account_sid = "AC2fe3275a720968152c8ace5b153283e3"
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def index(request):
    user_phone = "13176930478"
    message = "Do you want to purchase the all-new Nike hyperzoom sweatpants?"
    '''
    client.messages.create(
        body=f'{message}',
        from_="+17816509335",
        to=f'+{user_phone}'
    )
    '''
    return HttpResponse(f"Text message sent!\n\n {message}")


'''
possible states the user could be in:
1. we don't know if the user has metadata or not
1. we have no user metadata
2.

'''

possibleStates = {

}


'''
def getUserState
'''


@csrf_exempt
def text_received(request):
    # getUserState(request.POST.get('From'))
    '''
    user = User.objects.create_user(username='Niraj',
                                    email='deyneeraj666.com',
                                    password='glass onion')
    '''
    print(request)
    return HttpResponse("Text received!")
