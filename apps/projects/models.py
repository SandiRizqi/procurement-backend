from django.db import models
from apps.core.models import TimeStampedModel
# Create your models here.# apps/projects/models.py
class Project(TimeStampedModel):
    STATUS = [
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    project_name = models.CharField(max_length=255)
    project_value = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS)

    def __str__(self):
        return self.project_name
