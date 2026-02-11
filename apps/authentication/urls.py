from django.urls import path
from .views import LoginView, PermissionListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('permissions/', PermissionListView.as_view(), name='permission-list'),
]
