from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = 'public-read'

    def _save(self, name, content):
        print(f"Attempting to upload: {name}")
        return super()._save(name, content)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
    default_acl = 'public-read'