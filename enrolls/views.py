from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Enrollment, LessonProgress
from .serializers import EnrollmentSerializer
from .utils import update_module_completion
from courses.models import Lesson


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'status']

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset

        if user.is_staff:  # Admin: see all
            pass
        else:
            qs = qs.filter(student__user=user, status="Enrolled")

        return qs.select_related("course").prefetch_related(
            "course__modules__lessons",
            "course__modules__lessons__user_progress",
            "course__modules__user_progress",
        )

    def perform_create(self, serializer):
        course = self.request.data.get("course")
        serializer.save(student=self.request.user.student, course_id=course)

    @action(detail=False, methods=['get'])
    def is_enrolled(self, request):
        user = request.user
        course_id = request.query_params.get('course')
        enrolled = Enrollment.objects.filter(student__user=user, course_id=course_id, status="Enrolled").exists()
        return Response({'enrolled': enrolled})

    # User Lesson Progress
    @action(detail=False, methods=['post'], url_path="user-lesson-progress")
    def user_lesson_progress(self, request):
        user = request.user
        lesson_id = request.data.get("lesson_id")
        completed = request.data.get("completed", True)

        if not lesson_id:
            return Response({"detail": "Lesson ID is Required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson Not Found!"}, status=status.HTTP_404_NOT_FOUND)

        # Save Progress for Student
        student = getattr(user, "student", None)
        if not student:
            return Response({"detail": "Only Students can Update Progress."}, status=status.HTTP_403_FORBIDDEN)

        progress, _ = LessonProgress.objects.get_or_create(student=student, lesson=lesson)
        progress.completed = completed
        progress.save()

        # Update Module Completion
        update_module_completion(student, lesson.module)

        return Response({"detail": "Lesson Progress Updated"}, status=status.HTTP_200_OK)