from rest_framework import viewsets, generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate

from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from email.mime.image import MIMEImage

from .serializers import TeacherSerializer, StudentSerializer, RegisterSerializer
from .models import Teacher, Student
import os


# Teacher View (Admin/Staff Only)
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Student View (Logged-in Students Only)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Student.objects.all()  # Admin can access all students
        return Student.objects.filter(user=user)  # Student can access their own info only

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Register View (Open to All)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "id": user.id,
            "username": user.username,
            "message": "You have Registered Successfully! Please Login to Continue."
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View (Open to All)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        # Determine fullname & related id (student/teacher/admin)
        if user.is_superuser:
            fullname = user.get_full_name() or user.username
            related_id = user.id
        elif hasattr(user, 'student'):
            fullname = user.student.fullname
            related_id = user.student.id
        elif hasattr(user, 'teacher'):
            fullname = user.teacher.fullname
            related_id = user.teacher.id
        else:
            fullname = user.get_full_name() or user.username
            related_id = user.id

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'uid': user.id,           # Always Django User ID
                'id': related_id,         # Related model id (student/teacher/admin)
                'fullname': fullname,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
        })

    return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Change Password View (For Logged-in Users)
class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"detail": "Current Password is Incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)


# Reset Password Request View (Sends Email with Token Link)
class ResetPasswordRequestView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this Email does not Exist!"}, status=status.HTTP_404_NOT_FOUND)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        frontend_url = getattr(settings, "FRONTEND_URL", None)

        if not frontend_url:
            raise ImproperlyConfigured("Frontend URL is not set in Your Django Settings!")

        try:
            fullname = user.student.fullname
        except Student.DoesNotExist:
            try:
                fullname = user.teacher.fullname
            except Teacher.DoesNotExist:
                fullname = "User"

        reset_link = f"{frontend_url}/reset-confirm/{uid}/{token}/"

        # HTML Template with embedded image (uses Content-ID)
        html_content = render_to_string("reset/reset_email.html", {
            "user": user, "fullname": fullname, "reset_link": reset_link, })

        plain_text = strip_tags(html_content)

        # New: Use EmailMultiAlternatives for inline image support
        email_msg = EmailMultiAlternatives(
            subject="Password Reset Requested for Your MQWI Account",
            body=plain_text,    # Plain-text Fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email_msg.attach_alternative(html_content, "text/html")     # Actual HTML email

        # New: Embed image inline using MIMEImage
        logo_path = os.path.join(settings.MEDIA_ROOT, 'images/logo/main-logo.png')
        with open(logo_path, 'rb') as f:
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<logo>')
            logo.add_header('Content-Disposition', 'inline', filename="main-logo.png")
            email_msg.attach(logo)

        email_msg.send()

        return Response({"detail": "Password Reset Link sent to Your Email."}, status=status.HTTP_200_OK)


# Reset Password Confirm View (Used after Clicking Link)
class ResetPasswordConfirmView(generics.GenericAPIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid Reset Link!"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or Expired Token!"}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("new_password")
        if not new_password:
            return Response({"detail": "New password not provided!"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been Reset Successfully."}, status=status.HTTP_200_OK)