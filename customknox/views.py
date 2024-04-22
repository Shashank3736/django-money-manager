from knox.views import LogoutAllView as KnoxLogoutAllView
from knox.auth import TokenAuthentication
from rest_framework.authentication import BasicAuthentication
# Create your views here.
class LogoutAllView(KnoxLogoutAllView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]