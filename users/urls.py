from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ( TeacherViewSet, StudentViewSet, register, login,
    ChangePasswordView, ResetPasswordRequestView, ResetPasswordConfirmView, )

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Auth Endpoints
    path('register', register, name='register'),
    path('login', login, name='login'),
    # Password Endpoints
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('reset-request', ResetPasswordRequestView.as_view(), name='reset_request'),
    path('reset-confirm/<uidb64>/<token>', ResetPasswordConfirmView.as_view(), name='reset_confirm'),    
]

# Add JWT Token Views
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    # POST /api/token/ → Get JWT token (login)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   # POST /api/token/refresh/ → Refresh token
]