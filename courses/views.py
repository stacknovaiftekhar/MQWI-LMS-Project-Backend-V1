from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import ValidationError
from .models import Category, Course, Feature, Module, Lesson
from .serializers import (CategorySerializer, CourseSerializer, FeatureSerializer, ModuleSerializer, LessonSerializer)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Admins can do anything.
    Everyone else can only read (GET).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS for everyone
        return request.user and request.user.is_staff  # Only admins for POST, PUT, DELETE


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        teacher_id = self.request.query_params.get('teacher')
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        return queryset


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['course__id']

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if Feature.objects.filter(course=course).exists():
            raise ValidationError("Features for this Course Already Exist.")
        serializer.save()


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]