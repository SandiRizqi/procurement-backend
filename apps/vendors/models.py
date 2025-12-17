from django.db import models
from apps.core.models import TimeStampedModel
from django.conf import settings
from apps.core.utils import generate_presigned_url, safe_name



def document_upload_to(instance, filename):
    env = getattr(settings, 'ENVIRONMENT', 'dev')
    vendor_name = safe_name(instance.vendor.name)
    return f"{env}/vendors/{vendor_name}/{filename}"


class Vendor(TimeStampedModel):
    VENDOR_TYPE = [
        ('PT', 'PT'),
        ('CV', 'CV'),
        ('BUMN', 'BUMN'),
        ('PERSONAL', 'Perorangan'),
    ]

    name = models.CharField(max_length=255, blank=False, null=False)
    npwp = models.CharField(max_length=50, unique=True, null=True, blank=True)
    vendor_type = models.CharField(max_length=20, choices=VENDOR_TYPE)
    address = models.TextField(blank=True, max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
  
    

class VendorDocument(TimeStampedModel):
    DOCUMENT_TYPE = [
        ('certificate', 'Certificate'),
        ('npwp', 'npwp'),
        ('portfolio', 'portfolio'),
    ]

    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='documents'
    )
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_upload_to)
    issued_date = models.DateField(null=True, blank=True)
    expired_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.vendor.name}-{self.document_type}-{self.title}'
    

    @property
    def signed_file_url(self):
        if not self.file:
            return None
        key = f"{settings.AWS_LOCATION}/{self.file.name}"
        return generate_presigned_url(
            key,
            expires_in=3600
        )
    
    
