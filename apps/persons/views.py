from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Person, PersonDocument
from .serializers import PersonSerializer, PersonDocumentSerializer
from django_filters.rest_framework import DjangoFilterBackend

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # bisa diganti custom permission

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'vendor__name': ['exact', 'icontains'],  # related field lookup
        'role': ['exact', 'icontains'],
    }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.full_name
        self.perform_destroy(instance)
        return Response(
            {"message": f"Person '{name}' berhasil dihapus."},
            status=status.HTTP_200_OK
        )


class PersonDocumentViewSet(viewsets.ModelViewSet):
    queryset = PersonDocument.objects.all()
    serializer_class = PersonDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
