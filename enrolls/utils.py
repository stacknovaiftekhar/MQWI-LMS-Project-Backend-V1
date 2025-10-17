from .models import ModuleProgress, LessonProgress

def update_module_completion(student, module):
    lessons = module.lessons.all()
    completed_count = LessonProgress.objects.filter(student=student, lesson__in=lessons, completed=True).count()
    
    if completed_count == lessons.count():
        ModuleProgress.objects.update_or_create(
            student=student, module=module,
            defaults={"completed": True}
        )
    else:
        # If Not All Lessons are Completed, Ensure Module Progress is Marked Incomplete
        ModuleProgress.objects.update_or_create(
            student=student, module=module,
            defaults={"completed": False}
        )