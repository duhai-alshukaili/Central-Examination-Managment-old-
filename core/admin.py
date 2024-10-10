from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from core.models import User, Department, Lecturer, Student

# Customizing the UserAdmin for your custom User model
@admin.register(User)
class UserAdmin(DefaultUserAdmin):  # Extend DefaultUserAdmin for proper password handling

    list_display = ('username', 'email', 'department', 'user_type', 'is_lecturer', 'is_invigilator', 'is_exam_committee_member')
    list_filter = ('user_type', 'department', 'is_lecturer', 'is_invigilator', 'is_exam_committee_member')
    search_fields = ('username', 'email')

    # Custom fieldsets for better organization in the admin interface
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Basic login fields (username and password)
        ('Personal Info', {
            'fields': ('user_type', 'prefix', 'first_name', 'middle_name', 'last_name', 'email' ,'gender', 'department')
        }),
        ('Lecturer Information', {
            'fields': ('is_lecturer', 'is_invigilator', 'is_exam_committee_member'),
            'classes': ('collapse',)  # Optional: collapse section if not needed for other users
        }),
        ('Non-Academic Staff Permissions', {
            'fields': ('can_create_users', 'can_approve_absence_excuses', 'can_view_all_statistics'),
            'classes': ('collapse',)  # Optional: collapse section
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    # Override the add fieldsets to include custom fields while using proper password handling
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'first_name', 'last_name', 'email'),
        }),
    )

# Register Lecturer as a proxy model with custom admin
@admin.register(Lecturer)
class LecturerAdmin(UserAdmin):
    list_display = ('username', 'email', 'department', 'user_type', 'is_lecturer', 'is_invigilator', 'is_exam_committee_member')
    list_filter = ('user_type', 'department', 'is_lecturer', 'is_invigilator', 'is_exam_committee_member')
    search_fields = ('username', 'email')

    def get_changeform_initial_data(self, request):
        # Pre-fill the user_type as "Academic Staff" when adding a Lecturer
        return {'user_type': User.ACADEMIC_STAFF, 'is_lecturer': True, 'is_invigilator': True}


# Register Student as a proxy model with custom admin
@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ('username', 'email', 'department', 'user_type')
    list_filter = ('user_type', 'department')
    search_fields = ('username', 'email')

    def get_changeform_initial_data(self, request):
        # Pre-fill the user_type as "Student" when adding a Student
        return {'user_type': User.STUDENT}

# Register the Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name',)
