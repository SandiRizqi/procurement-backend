from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TenagaAhliViewSet, TenagaAhliDocumentViewSet

router = DefaultRouter()
router.register(r'tenaga-ahli', TenagaAhliViewSet, basename='tenaga-ahli')
router.register(r'tenaga-ahli-documents', TenagaAhliDocumentViewSet, basename='tenaga-ahli-document')

urlpatterns = [
    path('', include(router.urls)),
]
