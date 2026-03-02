from django.db import models
from apps.core.models import TimeStampedModel
from django.conf import settings
from apps.core.utils import generate_presigned_url, safe_name


def document_upload_to(instance, filename):
    env = getattr(settings, 'ENVIRONMENT', 'dev')
    person_name = safe_name(instance.person.nama_lengkap)
    return f"{env}/persons/{person_name}/{filename}"

# Create your models here.
class TenagaAhli(TimeStampedModel):
    nama_lengkap = models.CharField(max_length=255, blank=False, null=False, unique=True)
    jabatan = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    skills = models.JSONField(default=list, blank=True, null=True)
    telepon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.nama_lengkap}-{self.jabatan}'


class TenagaAhliDocument(TimeStampedModel):
    DOCUMENT_TYPE = [
        ('cv', 'CV'),
        ('sertifikat', 'sertifikat'),
        ('lainnya', 'lainnya')
    ]

    person = models.ForeignKey(
        TenagaAhli, on_delete=models.CASCADE, related_name='documents'
    )
    type = models.CharField(max_length=20, choices=DOCUMENT_TYPE)
    judul = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_upload_to)
    issued_date = models.DateField(null=True, blank=True)
    expired_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.judul}-{self.person.nama_lengkap}'
    
    @property
    def signed_file_url(self):
        if not self.file:
            return None
        key = f"{settings.AWS_LOCATION}/{self.file.name}"
        return generate_presigned_url(
            key,
            expires_in=3600
        )
    
