from django.test.client import RequestFactory
from django.test import TestCase

from send_bandwidth_message import views

from unittest import mock


class SendBandwidthMessagesTestCase(TestCase):
    def test_get_destination(self):
        mock_request = mock.Mock()
        mock_request.POST.get.return_value = "12345@test.com"
        expected_destination = "12345"

        destination = views.get_destination(mock_request)

        mock_request.POST.get.assert_called_with('recipient')
        self.assertEqual(destination, expected_destination)

    def test_get_message_stripped_text(self):
        mock_request = mock.Mock()
        mock_request.POST.__iter__ = mock.Mock(return_value=iter(["stripped-text", "stripped-signature"]))
        mock_request.POST.get.return_value = "12345"
        expected_message = "12345"

        message = views.get_message(mock_request)

        mock_request.POST.get.assert_called_with('stripped-text')
        self.assertEqual(message, expected_message)

    def test_get_message_stripped_signature(self):
        mock_request = mock.Mock()
        mock_request.POST.__iter__ = mock.Mock()
        mock_request.POST.__iter__.side_effect = [iter(["None"]), iter(["stripped-signature"])]
        mock_request.POST.get.return_value = "12345"
        expected_message = "12345"

        message = views.get_message(mock_request)

        mock_request.POST.get.assert_called_with('stripped-signature')
        self.assertEqual(message, expected_message)

    def test_get_message_body_plain(self):
        mock_request = mock.Mock()
        mock_request.POST.__iter__ = mock.Mock(return_value=iter([]))
        mock_request.POST.get.return_value = "12345"
        expected_message = "12345"

        message = views.get_message(mock_request)

        mock_request.POST.get.assert_called_with('body-plain')
        self.assertEqual(message, expected_message)
