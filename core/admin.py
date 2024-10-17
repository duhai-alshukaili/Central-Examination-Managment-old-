from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from core.models import User, Department, Lecturer, Student
from core.models import Course, Section, Room

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

    def get_queryset(self, request):
        """
        Override the queryset to only display users with 'academic' user_type.
        """
        qs = super().get_queryset(request)
        return qs.filter(user_type=User.ACADEMIC_STAFF)

    def get_changeform_initial_data(self, request):
        # Pre-fill the user_type as "Academic Staff" when adding a Lecturer
        return {'user_type': User.ACADEMIC_STAFF, 'is_lecturer': True, 'is_invigilator': True}


# Register Student as a proxy model with custom admin
@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ('username', 'email', 'department', 'user_type')
    list_filter = ('user_type', 'department')
    search_fields = ('username', 'email')

    def get_queryset(self, request):
        """
        Override the queryset to only display users with 'student' user_type.
        """
        qs = super().get_queryset(request)
        return qs.filter(user_type=User.STUDENT)

    def get_changeform_initial_data(self, request):
        # Pre-fill the user_type as "Student" when adding a Student
        return {'user_type': User.STUDENT}

# Register the Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Fields to display in the course list view
    list_display = ('code', 'name', 'coordinator', 'department')
    list_filter = ('department',)  # Add filter by department
    search_fields = ('code', 'name')  # Enable searching by course code and name

    # Optional: Customize the form layout in the admin
    fieldsets = (
        (None, {
            'fields': ('code', 'name', 'coordinator', 'department'),
        }),
    )

    # Override the form field's queryset for the coordinator field
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "coordinator":
            kwargs["queryset"] = User.objects.filter(user_type=User.ACADEMIC_STAFF)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    # Fields to display in the section list view
    list_display = ('course', 'number', 'lecturer')
    list_filter = ('course__department', 'lecturer')  # Filter by department and lecturer
    search_fields = ('course__code', 'course__name')  # Enable search by course code and name

    # Optional: Customize the form layout in the admin
    fieldsets = (
        (None, {
            'fields': ('course', 'number', 'lecturer'),
        }),
    )

    # Override the form field's queryset for the lecturer field
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "lecturer":
            kwargs["queryset"] = User.objects.filter(user_type=User.ACADEMIC_STAFF)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('label', 'room_type_display', 'campus', 'capacity', 'block')

    # Fields to filter by in the right sidebar
    list_filter = ('room_type', 'campus', 'block')

    # Enable searching by label and block
    search_fields = ('label', 'block')

    # Customize the form field's display name for room_type
    def room_type_display(self, obj):
        return dict(Room.ROOM_TYPE_CHOICES).get(obj.room_type, 'Unknown')
    room_type_display.short_description = 'Room Type'