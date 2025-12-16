from django.db import models
from apps.core.models import TimeStampedModel
from django.conf import settings
from apps.core.utils import generate_presigned_url, safe_name


def document_upload_to(instance, filename):
    env = getattr(settings, 'ENVIRONMENT', 'dev')
    vendor_name = safe_name(instance.person.vendor.name)
    person_name = safe_name(instance.person.full_name)
    return f"{env}/vendors/{vendor_name}/persons/{person_name}/{filename}"

# Create your models here.
class Person(TimeStampedModel):
    vendor = models.ForeignKey(
        'vendors.Vendor', on_delete=models.CASCADE, related_name='persons'
    )
    full_name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    role = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.vendor.name}-{self.full_name}'


class PersonDocument(TimeStampedModel):
    DOCUMENT_TYPE = [
        ('cv', 'CV'),
        ('certificate', 'Certificate'),
    ]

    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='documents'
    )
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_upload_to)
    issued_date = models.DateField(null=True, blank=True)
    expired_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.person.vendor.name}-{self.person.full_name}'
    
    @property
    def signed_file_url(self):
        if not self.file:
            return None
        key = f"{settings.AWS_LOCATION}/{self.file.name}"
        return generate_presigned_url(
            key,
            expires_in=3600
        )
    
