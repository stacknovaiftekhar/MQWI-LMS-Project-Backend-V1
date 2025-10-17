from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactInfoView, SocialLinksView, WalletInfoViewSet, BankDetailViewSet

router = DefaultRouter()
router.register(r'wallet-info', WalletInfoViewSet)
router.register(r'bank-detail', BankDetailViewSet)

urlpatterns = [
    path('contact-info', ContactInfoView.as_view(), name='contact-info'),
    path('social-links', SocialLinksView.as_view(), name='social-links'),
    path('', include(router.urls)),
]