"""
Implementation of SMS to Email integration using the Bandwidth messaging API
and Mailgun API. This route allows an end user to text a Bandwidth number
that is set up to make a POST request on this route,
and have the contents of that text be received by an email through the Mailgun
API.  The email received will be sent from <number>@<domain> where
<number> is the phone number of the end user sending the text.
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json
import os

MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
MAILGUN_EMAIL_DOMAIN = os.environ['MAILGUN_EMAIL_DOMAIN']
DESTINATION_EMAIL = os.environ['DESTINATION_EMAIL']


def get_message(post_request):
    """
    Takes a POST request and extracts the message from it.

    :post_request :HttpRequest A Django POST HttpRequest

    :return :String The message from the text
    """
    return json.loads(post_request.body)["text"]


def get_source(post_request):
    """
    Takes a POST request and extracts the source from it.

    :post_request :HttpRequest A Django POST HttpRequest

    :return :String The source from the text
    """
    return json.loads(post_request.body)["from"]


def send_message(message, source_email, destination, url, api_key, request_function):
    """
    Sends the message using the Mailgun API.

    :message :String The message to be sent
    :source :String The source (phone number) of the message
    :destination :String The (email) destination of the message
    """
    request_function.post(
        url,
        auth=("api", api_key),
        data={
            "from": source_email,
            "to": destination,
            "text": message
        })


@csrf_exempt
def send_mailgun_email(request):
    if request.method == "GET":
        return HttpResponse('hello')

    elif request.method == "POST":
        # Get information to send message
        destination = DESTINATION_EMAIL
        message = get_message(request)
        source = get_source(request)

        # Send message
        mailgun_url = "https://api.mailgun.net/v3/{}/messages".format(
            MAILGUN_EMAIL_DOMAIN
        )
        source_email = "{}@{}".format(source, MAILGUN_EMAIL_DOMAIN)
        send_message(
            message,
            source_email,
            destination,
            mailgun_url,
            MAILGUN_API_KEY,
            requests
        )

        return HttpResponse("success")
