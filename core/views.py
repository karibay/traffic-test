from rest_framework import viewsets

from .serializers import ApplicationSerializer
from .models import Application


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
