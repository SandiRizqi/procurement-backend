from django.db import models
from apps.core.models import TimeStampedModel
from apps.projects.models import Project
from django.conf import settings
from apps.core.utils import generate_presigned_url, safe_name


def document_upload_to(instance, filename):
    env = getattr(settings, 'ENVIRONMENT', 'dev')
    vendor_name = safe_name(instance.vendor.name)
    project_name = safe_name(instance.procurement.project.project_name)
    return f"{env}/vendors/{vendor_name}/{project_name}/{filename}"


# apps/procurements/models.py
class Procurement(TimeStampedModel):
    TYPE = [
        ('lelang', 'Lelang'),
        ('penunjukan', 'Penunjukan Langsung'),
    ]

    STATUS = [
        ('open', 'Open'),
        ('evaluation', 'Evaluation'),
        ('winner_selected', 'Winner Selected'),
        ('failed', 'Failed'),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='procurements'
    )
    procurement_type = models.CharField(max_length=20, choices=TYPE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS)


    def __str__(self):
        return f'{self.project.project_name}'


class ProcurementParticipant(TimeStampedModel):
    STATUS = [
        ('submitted', 'Submitted'),
        ('evaluated', 'Evaluated'),
        ('winner', 'Winner'),
        ('loser', 'Loser'),
    ]

    procurement = models.ForeignKey(
        Procurement, on_delete=models.CASCADE, related_name='participants'
    )
    vendor = models.ForeignKey(
        'vendors.Vendor', on_delete=models.CASCADE
    )
    bid_value = models.DecimalField(max_digits=15, decimal_places=2)
    file = models.FileField(upload_to=document_upload_to, null=True,)
    submission_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS)

    class Meta:
        unique_together = ('procurement', 'vendor')

    def __str__(self):
        return f"{self.procurement}-{self.vendor}"
    
    @property
    def signed_file_url(self):
        if not self.file:
            return None
        key = f"{settings.AWS_LOCATION}/{self.file.name}"
        return generate_presigned_url(
            key,
            expires_in=3600
        )

