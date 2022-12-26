# from django.contrib.auth.models import User
from texts.models import Recipient, Product, ProductCategory
from django.http import HttpResponse
from twilio.rest import Client
import os
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from django.shortcuts import get_object_or_404


account_sid = "AC2fe3275a720968152c8ace5b153283e3"
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

DEBUG = True


def send_message(phone: str, message: str):
    if(DEBUG):
        print(f"Phone: {phone}\n\n Message: {message}")
    else:
        client.messages.create(
            body=f'{message}',
            from_="+17816509335",
            to=f'{phone}'
        )


@ csrf_exempt
def index(request):
    productCategory = request.POST.get('ProductCategory')
    recipientPhone = request.POST.get('RecipientPhone')

    productCategory = ProductCategory.objects.get(name=productCategory)

    targetCustomer = Recipient.objects.get(phone=recipientPhone)
    targetCustomer.current_offering = productCategory
    targetCustomer.save()

    message = f"Do you want to purchase the {productCategory.name}? Respond YES to purchase or NO to decline."
    send_message(recipientPhone, message)

    return HttpResponse(f"Text message sent!\n\n {message}")


def getUserMetadata(currUser: Recipient):
    offeringType = currUser.current_offering.type
    if(offeringType == "Bottoms"):
        return currUser.bottom_sizes
    elif(offeringType == "Tops"):
        return currUser.top_sizes
    else:
        return None


def paymentDataAlreadyStored():
    return False

# Very basic data checking


def sentDataIsPaymentData():
    return True


def stripeConfirmedData():
    return True
# Takes the user's current state AND a text message THEN returns the next state
# We should do next_state if this state is a process sate with no presence in State2Response
# We should not do next_state if this state has a presence
# We should do send_message + next_state if this state is a process state with a text message


def next_text_state(currUser: Recipient, response: str):
    state = currUser.state
    if state == "UnknownPreference":
        if response == "YES":
            currUser.state = "AffirmativePurchase"
            currUser.save()
            return next_text_state(currUser, response)
        elif response == "NO":
            currUser.state = "NegativePurchase"
            currUser.save()
            return next_text_state(currUser, response)
        else:
            return "InvalidState"
    elif state == "AffirmativePurchase":
        if getUserMetadata(currUser) != None:
            return "MetadataExists"
        else:
            return next_text_state("NoneOrIncorrectMetadata", response)
    elif state == "NegativePurchase":
        send_message(currUser.phone, "Thanks for your time!")
        return "Terminated"
    elif state == "MetadataExists":
        if response == "YES":
            currUser.state = "CorrectMetadata"
            currUser.save()
            return next_text_state(currUser, response)
        elif response == "NO":
            return "NoneOrIncorrectMetadata"
        else:
            return "InvalidState"
    elif state == "NoneOrIncorrectMetadata":
        if response == "S" or response == "M" or response == "L" or response == "XL":
            if(currUser.current_offering.type == "Tops"):
                currUser.top_sizes = response
            elif currUser.current_offering.type == "Bottoms":
                currUser.bottom_sizes = response
            else:
                raise Exception("Invalid offering type")
            currUser.save()
            return "MetadataExists"
        else:
            return "InvalidState"
    elif state == "CorrectMetadata":
        if paymentDataAlreadyStored():
            currUser.state = "PaymentAndMetadataCorrect"
            currUser.save()
            return next_text_state(currUser, response)
        else:
            return "NoPaymentData"
    elif state == "NoPaymentData":
        # i.e. did they send credit card info or just random stuff::
        if sentDataIsPaymentData():
            currUser.state = "PaymentRequested"
            currUser.save()
            return next_text_state(currUser, response)
        else:
            currUser.state = "InvalidPaymentDetails"
            currUser.save()
            return next_text_state(currUser, response)
    elif state == "PaymentRequested":
        # Stripe confirms that their data is good
        if stripeConfirmedData():
            currUser.state = "PaymentAndMetadataCorrect"
            currUser.save()
            return next_text_state(currUser, response)
        else:
            currUser.state = "InvalidPaymentDetails"
            currUser.save()
            return next_text_state(currUser, response)
    elif state == "InvalidPaymentDetails":
        send_message(currUser.phone, "Invalid credit card info!")
        return "NoPaymentData"
    elif state == "PaymentAndMetadataCorrect":
        send_message(currUser.phone, "Purchase made. Here is your receipt: ")
        return "Terminated"
    elif state == "Terminated":
        return "Terminated"
    else:
        return next_text_state(currUser, response)


# Takes the user's upcoming state and returns the appropriate prompt
def State2Response(recipient: Recipient, state: str):
    if state == "InvalidState":
        return "Sorry, I didn't quite understand that. Please try again."
    elif state == "MetadataExists":
        return "Is " + getUserMetadata(recipient) + " the correct size? Respond YES if it is or NO if not."
    elif state == "NoneOrIncorrectMetadata":
        return "What size would you like? Respond S, M, L, or XL."
    # elif state == "CorrectMetadata":
        # return "Is your credit card information 6969 - 6969 - 6969 - 6969 correct? Respond YES if it is or NO if not."
    elif state == "NoPaymentData":
        return "Please enter your credit card information."

    elif state == "InvalidPaymentDetails":
        return "Sorry, your credit card information was invalid. Please try again."
    elif state == "PaymentAndMetadataCorrect":
        # Charge their credit card
        # Senc a receipt message
        return "Great, your order of a _ is on the way!"
    elif state == "Terminated":
        return ""
    else:
        # this shouldn't happen
        raise Exception("Invalid State: " + state)


@ csrf_exempt
def text_received(request):
    phone = request.POST.get('From')
    body = request.POST.get('Body')
    recipient = Recipient.objects.filter(
        phone=phone)

    if len(recipient) == 0:
        return HttpResponse("No recipient found")
    elif len(recipient) > 1:
        return HttpResponse("Multiple recipients found")

    recipient = recipient[0]
    prevState = recipient.state
    # get the user's next state that requires a prompt
    nextTextState = next_text_state(recipient, body)

    # set the user's new state
    recipient.state = nextTextState
    recipient.save()

    resp = MessagingResponse()

    if(nextTextState == "Terminated" and prevState == "Terminated"):
        resp.message("No prompt associated with message")
        return str(resp)

    response = State2Response(recipient, nextTextState)
    resp.message(response)
    ### TEST ###
    send_message("+13176930478", response)
    ### TEST ###

    # if(nextTextState == "Terminated" and prevState != "Terminated"):
    # the og: https://support.twilio.com/hc/en-us/articles/223134127-Receive-SMS-and-MMS-Messages-without-Responding
    # resp.message("")
    # return str(resp)

    return HttpResponse(str(resp))
