"""
Source code from Boutique Ado walkthrough.

Refactored for better readability, maintainability, and compliance with
Django best practices.
"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Custom storage backend for handling static files with S3.
    Uses the settings defined in the Django project for the S3 bucket.

    Attributes:
        location (str): The location within the S3 bucket where static files are stored.
        default_acl (str): Access control list for static files. Defaults to 'public-read'.
    """
    location = settings.STATICFILES_LOCATION
    default_acl = 'public-read'

    def _save(self, name, content):
        return super()._save(name, content)


class MediaStorage(S3Boto3Storage):
    """
    Custom storage backend for handling media files with S3.
    Uses the settings defined in the Django project for the S3 bucket.

    Attributes:
        location (str): The location within the S3 bucket where media files are stored.
        file_overwrite (bool): Determines whether files with the same name will be overwritten.
                               Defaults to False.
        default_acl (str): Access control list for media files. Defaults to 'public-read'.
    """
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
    default_acl = 'public-read'

    def _save(self, name, content):
        return super()._save(name, content)