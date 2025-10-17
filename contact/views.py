from rest_framework import permissions, viewsets
from .models import ContactInfo, SocialLink, WalletInfo, BankDetail
from .serializers import ContactInfoSerializer, SocialLinkSerializer, WalletInfoSerializer, BankDetailSerializer
from .utils import SingletonAPIView


# class AdminOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_staff

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Anyone can read (GET, HEAD, OPTIONS)
        return request.user and request.user.is_staff  # Only admin can POST/PUT/DELETE


class ContactInfoView(SingletonAPIView):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = [IsAdminOrReadOnly]


class SocialLinksView(SingletonAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAdminOrReadOnly]


class WalletInfoViewSet(viewsets.ModelViewSet):
    queryset = WalletInfo.objects.all()
    serializer_class = WalletInfoSerializer    
    permission_classes = [IsAdminOrReadOnly]


class BankDetailViewSet(viewsets.ModelViewSet):
    queryset = BankDetail.objects.all()
    serializer_class = BankDetailSerializer    
    permission_classes = [IsAdminOrReadOnly]