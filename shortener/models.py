from django.db import models
from django.utils import timezone


class Url(models.Model):
    url_id = models.AutoField(
        primary_key=True, editable=False
    )  # Auto-incrementing integer field used as primary key.
    original_url = (
        models.URLField()
    )  # URLField used to store the original URL.
    short_url = models.CharField(
        max_length=15, unique=True
    )  # CharField used to store the shortened URL, with a maximum length of 15 characters and unique constraint.
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # DateTimeField used to store the creation time of the URL.
    expires_at = models.DateTimeField(
        null=True, blank=True
    )  # DateTimeField used to store the expiration time of the URL. Optional, can be null or blank.

    class Meta:
        ordering = [
            "-created_at"
        ]  # Order URLs by creation time, in descending order.

    def __str__(self):
        return f"Original: {self.original_url}, Shortened: {self.short_url}"  # Return string representation of the URL object.

    @property
    def expired(self):
        # Property that returns whether the URL has expired or not, by comparing the current time to the expiration time. Returns a boolean value.
        return self.expires_at and timezone.now() > self.expires_at
