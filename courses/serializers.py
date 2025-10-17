from rest_framework import serializers
from .models import Category, Course, Feature, Module, Lesson
from enrolls.models import LessonProgress, ModuleProgress

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Feature Serializer
class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    teacher_name_bn = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    feature_id = serializers.IntegerField(source='features.id', read_only=True)
    features = FeatureSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_teacher_name_bn(self, obj):
        return obj.teacher.name_bn if obj.teacher else None
    
    def get_category_name(self, obj):
        return obj.category.name


# Lesson Serializer
class LessonSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'module', 'title', 'video', 'sheet', 'content', 'completed']

    def get_completed(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            return False

        student = getattr(user, "student", None)
        if not student:
            return False

        return LessonProgress.objects.filter(student=student, lesson=obj, completed=True).exists()


# Module Serializer
class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'description', 'order', 'lessons', 'completed']

    def get_completed(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            return False

        student = getattr(user, "student", None)
        if not student:
            return False

        return ModuleProgress.objects.filter(student=student, module=obj, completed=True).exists()