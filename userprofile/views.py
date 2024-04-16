from rest_framework import viewsets, permissions
from .serializers import ProfileSerializer
from .models import Profile
# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)