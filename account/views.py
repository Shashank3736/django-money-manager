from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser as User
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]
    partial = True

    def get_queryset(self):
        if self.request.user:
            return User.objects.filter(id=self.request.user.id)
        return []

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)
