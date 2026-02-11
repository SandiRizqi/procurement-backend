from rest_framework import viewsets, permissions
from .models import Person, PersonDocument
from .serializers import PersonSerializer, PersonDocumentSerializer
from django_filters.rest_framework import DjangoFilterBackend

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]  # bisa diganti custom permission

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'vendor__name': ['exact', 'icontains'],  # related field lookup
        'role': ['exact', 'icontains'],
    }


class PersonDocumentViewSet(viewsets.ModelViewSet):
    queryset = PersonDocument.objects.all()
    serializer_class = PersonDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
