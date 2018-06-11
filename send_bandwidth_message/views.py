"""
Implementation of SMS to Email integration using the Bandwidth messaging API
and Mailgun API. This route allows a user to send an email to their domain
in the format <number>@<domain>, and with a Mailgun filter set up
to make a POST request on this route, and have the contents of that
email be received by a text message via the Bandwidth messaging API.
The text will be sent to the phone number in the destination email.

Example: sending an email with the message "Hi John" to
+19193334444@my_domain.com will send a text message with the contents
"Hi John" through a Bandwidth number to +19193334444
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bandwidth import messaging

import json
import os

BANDWIDTH_USER_ID = os.environ['BANDWIDTH_USER_ID']
BANDWIDTH_API_TOKEN = os.environ['BANDWIDTH_API_TOKEN']
BANDWIDTH_API_SECRET = os.environ['BANDWIDTH_API_SECRET']
BANDWIDTH_NUMBER = os.environ['BANDWIDTH_NUMBER']


def get_destination(post_request):
    """
    Takes a POST request from Mailgun and extracts the
    phone number destination from it.

    For this app, we are expecting emails intercepted by Mailgun to be in
    the format <number>@<domain> with the phone number destination being
    the <number> part.

    :post_request A Django POST HttpRequest

    :return :String The destination from the POST request
    """
    return post_request.POST.get('recipient').split('@')[0]


def get_message(post_request):
    """
    Takes a POST request and extracts the message

    Priority of message:
        stripped-text
        stripped-signature
        body-plain

    :post_request A Django POST HttpRequest

    :return :String The message from the POST request
    """
    lst = ['stripped-text', 'stripped-signature']
    for value in lst:
        if value in post_request.POST:
            return post_request.POST.get(value)

    return post_request.POST.get('body-plain')


@csrf_exempt
def send_bandwidth_message(request):
    if request.method == "GET":
        return HttpResponse('hello')

    elif request.method == "POST":
        # Get destination and message from the POST request
        destination = get_destination(request)
        message = get_message(request)

        # Set up messaging client
        messaging_client = messaging.Client(
            BANDWIDTH_USER_ID,
            BANDWIDTH_API_TOKEN,
            BANDWIDTH_API_SECRET)
        source_number = BANDWIDTH_NUMBER

        # Send message
        messaging_client.send_message(
            from_=source_number,
            to=destination,
            text=message
        )

        return HttpResponse("success")
