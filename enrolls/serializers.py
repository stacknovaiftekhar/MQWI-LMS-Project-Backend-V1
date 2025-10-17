# enroll/serializers.py
from rest_framework import serializers
from .models import Enrollment
from courses.serializers import CourseSerializer, ModuleSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.fullname', read_only=True)
    course = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'enrolled_at', 'status']
        read_only_fields = ['enrolled_at', 'status']

    def get_course(self, obj):
        """
        Return full course data, including modules + lessons + progress,
        with request context passed down.
        """
        from courses.models import Module  # Avoid Circular Import

        modules = Module.objects.filter(course=obj.course).order_by('order')
        course_data = CourseSerializer(obj.course, context=self.context).data
        course_data['modules'] = ModuleSerializer(modules, many=True, context=self.context).data
        return course_data