from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from .models import Url
from .views import generate_random_specific_length_string


class UrlModelTestCase(TestCase):
    """
    Test case for the Url model.
    """

    def setUp(self):
        self.url = Url.objects.create(
            original_url="http://www.example.com/",
            short_url=generate_random_specific_length_string(),
        )

    def test_url_str(self):
        """
        Test the string representation of the Url model.
        """
        self.assertEqual(
            str(self.url),
            f"Original: {self.url.original_url}, Shortened: {self.url.short_url}",
        )

    def test_url_expired(self):
        """
        Test the expired property of the Url model when the expiration date is in the past.
        """
        self.url.expires_at = timezone.now() - timezone.timedelta(days=1)
        self.assertTrue(self.url.expired)

    def test_url_not_expired(self):
        """
        Test the expired property of the Url model when the expiration date is in the future.
        """
        self.url.expires_at = timezone.now() + timezone.timedelta(days=1)
        self.assertFalse(self.url.expired)


class ShortenUrlAPIViewTestCase(TestCase):
    """
    Test case for the ShortenUrlAPIView.
    """

    def setUp(self):
        self.client = Client()

    def test_shorten_url_post(self):
        """
        Test the creation of a shortened URL with a POST request.
        """
        data = {"original_url": "http://www.example.com/"}
        response = self.client.post(
            reverse("shortener:shorten_url"),
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("short_url" in response.data)

    def test_shorten_url_post_custom_alias(self):
        """
        Test the creation of a shortened URL with a custom alias with a POST request.
        """
        data = {
            "original_url": "http://www.example.com/",
            "custom_alias": "custom",
        }
        response = self.client.post(
            reverse("shortener:shorten_url"),
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["short_url"].split("/")[-1], "custom")

    def test_shorten_url_post_custom_alias_taken(self):
        """
        Test the creation of a shortened URL with a taken custom alias with a POST request.
        """
        url = Url.objects.create(
            original_url="http://www.example.com/",
            short_url="custom",  # existing custom alias
        )
        data = {
            "original_url": "http://www.example.com/",
            "custom_alias": "custom",
        }
        response = self.client.post(
            reverse("shortener:shorten_url"),
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("error" in response.data)

    def test_shorten_url_post_invalid(self):
        """
        Test the creation of a shortened URL with an invalid URL with a POST request.
        """
        data = {"original_url": "invalid"}
        response = self.client.post(
            reverse("shortener:shorten_url"),
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("error" in response.data)


class RedirectShortenUrlAPIViewTestCase(TestCase):
    """
    Test case for the RedirectShortenUrlAPIView.
    """

    def setUp(self):
        self.client = Client()
        self.url = Url.objects.create(
            original_url="http://www.example.com/",
            short_url=generate_random_specific_length_string(),
        )

    def test_redirect_shorten_url_get(self):
        """
        Test the redirection to the original URL with a GET request to a shortened URL.
        """
        response = self.client.get(
            reverse(
                "shortener:redirect_shorten_url",
                kwargs={"short_url": self.url.short_url},
            ),
        )
        self.assertRedirects(
            response, self.url.original_url, fetch_redirect_response=False
        )

    def test_redirect_shorten_url_get_not_found(self):
        """
        Test the response when attempting to redirect to a nonexistent shortened URL.
        """
        response = self.client.get(
            reverse(
                "shortener:redirect_shorten_url",
                kwargs={"short_url": "invalid"},
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
