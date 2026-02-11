from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PersonViewSet, PersonDocumentViewSet

router = DefaultRouter()
router.register(r'persons', PersonViewSet, basename='person')
router.register(r'person-documents', PersonDocumentViewSet, basename='person-document')

urlpatterns = [
    path('', include(router.urls)),
]
