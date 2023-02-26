import string
import random

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from .serializers import UrlSerializer
from .models import Url


# IndexAPIView to render the index page
class IndexAPIView(APIView):
    # Use JSON and TemplateHTML renderer classes
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    # GET method to render the index.html template
    def get(self, request):
        return Response(
            status=status.HTTP_200_OK,
            template_name="index.html",
        )


# Function to generate a random string of specified length
def generate_random_specific_length_string(length=10):
    """Generate a random string of the specified length."""
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def validate_alias(alias):
    """Validates if the alias can be a short url"""
    # If the length of the alias exceeds the maximum length of the short url
    if len(alias) > 15:
        return False
    alphanums = string.ascii_lowercase + string.digits
    # If alias contains any non chars other than above alphanums
    try:
        if any(c not in alphanums for c in alias):
            return False
    except Exception as e:
        return False
    return True


# ShortenURLAPIView to generate a short URL for the specified original URL
class ShortenURLAPIView(APIView):
    """
    Generate a short URL for the specified original URL.

    Request Method: POST
    Request Body:
    {
        "original_url": "https://www.example.com/path/to/resource",
        "custom_alias": "example",
        "expires_at": "2023-03-31 12:00:00"
    }
    Response Body:
    {
        "original_url": "https://www.example.com/path/to/resource",
        "short_url": "http://localhost:8000/example",
    }

    - `original_url` (string, required): The original URL to shorten.
    - `custom_alias` (string, optional): Optional custom alias for the short URL.
    - `expires_at` (string, optional): Optional expiration date/time for the short URL in `YYYY-MM-DD HH:MM:SS` format.

    If a custom alias is provided and it is already in use, the API will return a `400 Bad Request` response with the following error message:
    {
        "error": "Custom alias already exists."
    }

    If an expiration date/time is provided and it is in the past, the API will return a `400 Bad Request` response with the following error message:
    {
        "error": "The specified expiration date/time is in the past."
    }
    """

    # POST method to shorten the provided URL
    def post(self, request):
        # Check if custom alias is provided
        custom_alias = request.data.get("custom_alias")
        if not custom_alias:
            custom_alias = None

        if custom_alias is not None:
            # Validating the alias
            if not validate_alias(custom_alias):
                return Response(
                    data={"error": "Custom alias is not valid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Check if the custom alias already exists in the database
            if Url.objects.filter(short_url=custom_alias).exists():
                return Response(
                    data={"error": "Custom alias already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Use the custom alias as the short URL
            short_url = custom_alias
        else:
            # Generate a random short URL
            short_url = generate_random_specific_length_string()

        # Create a dictionary with the original URL, optional expiration date, and the short URL
        data = {
            "original_url": request.data.get("original_url"),
            "expires_at": request.data.get("expires_at"),
            "short_url": short_url,
        }
        # If no expiration date was provided, set it to None
        if not data["expires_at"]:
            data["expires_at"] = None

        # Create an instance of the UrlSerializer with the dictionary and the short URL
        serializer = UrlSerializer(data=data)
        # Check if the serializer is valid
        if serializer.is_valid():
            serializer.save()

            # Build the shortened URL and return a success response
            shortened_url = request.build_absolute_uri("/") + short_url
            return Response(
                data={
                    "short_url": shortened_url,
                    "original_url": request.data["original_url"],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={
                "error": "Couldn't shorten the url",
                **serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class RedirectShortenUrlAPIView(APIView):
    """
    API view to redirect to the original URL corresponding to the specified short URL.
    """

    def get(self, request, short_url):
        """
        Handle GET requests to the API view.

        Args:
            request (HttpRequest): the HTTP request object
            short_url (str): the short URL to redirect to the original URL

        Returns:
            A redirect response to the original URL if the short URL exists, or a 404 error response.

        """
        try:
            # Attempt to retrieve the URL object from the short URL parameter
            url = Url.objects.get(short_url=short_url)
        except Url.DoesNotExist:
            # If the URL object does not exist, return a 404 error response
            return Response(
                data={"error": "No such shortened url exists."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # If the URL object is expired, return a 404 error
        if url.expired:
            return Response(
                data={
                    "error": "The shorten url has expired and doesn't redirect anymore."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # If the URL object exists, redirect to the original URL using the Django redirect shortcut
        return redirect(url.original_url)
