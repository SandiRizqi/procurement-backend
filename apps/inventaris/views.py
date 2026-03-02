from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import TenagaAhli, TenagaAhliDocument
from .serializers import TenagaAhliDocumentSerializer, TenagaAhliSerializer
from django_filters.rest_framework import DjangoFilterBackend

class TenagaAhliViewSet(viewsets.ModelViewSet):
    queryset = TenagaAhli.objects.all()
    serializer_class = TenagaAhliSerializer
    permission_classes = [permissions.IsAuthenticated,] #permissions.DjangoModelPermissions]  # bisa diganti custom permission

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'jabatan': ['exact', 'icontains'],
    }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.nama_lengkap
        self.perform_destroy(instance)
        return Response(
            {"message": f"Tenaga Ahli '{name}' berhasil dihapus."},
            status=status.HTTP_200_OK
        )


class TenagaAhliDocumentViewSet(viewsets.ModelViewSet):
    queryset = TenagaAhliDocument.objects.all()
    serializer_class = TenagaAhliDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
