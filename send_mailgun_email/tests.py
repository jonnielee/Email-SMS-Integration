from django.test.client import RequestFactory
from django.test import TestCase

from send_mailgun_email import views

from unittest import mock
import json
import requests
import os


class SendBandwidthMessagesTestCase(TestCase):
    def test_get_message(self):
        mock_request = mock.Mock()
        expected_message = "12345"
        mock_request.body = json.dumps({"text": expected_message})

        message = views.get_message(mock_request)

        self.assertEqual(message, expected_message)

    def test_get_source(self):
        mock_request = mock.Mock()
        expected_message = "12345"
        mock_request.body = json.dumps({"from": expected_message})

        message = views.get_source(mock_request)

        self.assertEqual(message, expected_message)

    def test_send_message(self):
        message = 'message'
        source_email = 'source'
        destination = 'destination'
        api_key = 'key'
        url = 'url'
        request_function = mock.Mock()
        views.send_message(
            message,
            source_email,
            destination,
            url,
            api_key,
            request_function
        )

        request_function.post.assert_called_with(
            url,
            auth=("api", api_key),
            data={
                "from": source_email,
                "to": destination,
                "text": message
            }
        )
