from rest_framework import viewsets, permissions
from .serializers import BudgetSerializer

# Create your views here.
class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.budgets.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
