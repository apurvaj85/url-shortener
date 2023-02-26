from ..models import Url
from django.utils import timezone


# Function to delete expired URLs from the database
def delete_expired_urls():
    # Get all expired URLs from the database
    expired_urls = Url.objects.filter(expires_at__lt=timezone.now())

    # Delete all expired URLs from the database
    expired_urls.delete()
