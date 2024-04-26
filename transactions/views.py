from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import TransactionSerializer, AccountSerializer, CategorySerializer
from django.utils import timezone
from .models import Transaction#, Account, Category
# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.accounts.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.categories.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date = request.query_params.get('date', None)
        if date:
            try:
                date = timezone.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return Response({'message': 'Invalid date format, should be YYYY-MM-DD'}, status=400)
        else:
            date = timezone.now()

        queryset = Transaction.objects.filter(user=self.request.user, datetime__year=date.year, datetime__month=date.month, datetime__day=date.day)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_month(self, request):
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)

        queryset = Transaction.objects.filter(user=self.request.user, datetime__year=year, datetime__month=month)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)