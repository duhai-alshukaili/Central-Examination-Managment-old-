from django.contrib import admin
from core.models import User, Department, Lecturer, Student

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'department', 'user_type', 'is_lecturer', 'is_invigilator', 'is_exam_committee_member')
    list_filter = ('user_type', 'department', 'is_lecturer', 'is_invigilator', 'is_exam_committee_member')
    search_fields = ('username', 'email')

    def get_list_display(self, request):
        # Customize list_display dynamically based on permissions if necessary
        return super().get_list_display(request)

    def get_list_filter(self, request):
        # Customize list_filter dynamically if necessary
        return super().get_list_filter(request)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name',)

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'department', 'user_type', 'is_lecturer', 'is_invigilator', 'is_exam_committee_member')
    list_filter = ('user_type', 'department', 'is_lecturer', 'is_invigilator', 'is_exam_committee_member')
    search_fields = ('username', 'email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'department', 'user_type')
    list_filter = ('user_type', 'department')
    search_fields = ('username', 'email')