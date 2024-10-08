from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255)  # Department name
    email = models.EmailField(null=True, blank=True)  # Nullable email
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Nullable phone number

    def __str__(self):
        return self.name
    
class User(AbstractUser):

    # Adding related_name to resolve the clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_users',  # Custom related name to avoid clash
        blank=True,
        help_text=('The groups this user belongs to. '
                   'A user will get all permissions granted to each of their groups.'),
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_users_permissions',  # Custom related name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    # User types
    STUDENT = 'student'
    ACADEMIC_STAFF = 'academic_staff'
    NON_ACADEMIC_STAFF = 'non_academic_staff'
    SENIOR_MANAGEMENT = 'senior_management'

    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (ACADEMIC_STAFF, 'Academic Staff'),
        (NON_ACADEMIC_STAFF, 'Non-Academic Staff'),
        (SENIOR_MANAGEMENT, 'Senior Management'),
    ]

    # Field to distinguish between students and different types of staff
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)

    # Basic data required by all users
    # Prefix choices
    PREFIX_CHOICES = [
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        ('Mrs', 'Mrs.'),
        ('Dr', 'Dr.'),
        ('Prof', 'Prof.'),
    ]

    # Gender choices
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    # New fields
    prefix = models.CharField(
        max_length=10, 
        choices=PREFIX_CHOICES, 
        null=True, 
        blank=True,  # Can be null
        verbose_name="Prefix"
    )
    
    first_name = models.CharField(
        max_length=150,  # Default max_length for first_name in Django
        verbose_name="First Name"
    )
    
    middle_name = models.CharField(
        max_length=150, 
        null=True, 
        blank=True,  # Can be null
        verbose_name="Middle Name"
    )
    
    last_name = models.CharField(
        max_length=150, 
        verbose_name="Last Name"
    )
    
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        null=True, 
        blank=True,  # Can be null
        verbose_name="Gender"
    )

    # Department foreign key
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)

    # Lecturer-specific fields
    is_lecturer = models.BooleanField(default=False)
    is_invigilator = models.BooleanField(default=False)
    is_exam_committee_member = models.BooleanField(default=False)  # For lecturers who are in the exam committee

    # Non-academic staff fields
    can_create_users = models.BooleanField(default=False)
    can_approve_absence_excuses = models.BooleanField(default=False)
    can_view_all_statistics = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Lecturer(User):
    class Meta:
        proxy = True
        verbose_name = "Lecturer"
        verbose_name_plural = "Lecturers"
    
    def save(self, *args, **kwargs):
        # Ensure that the lecturer flag is always set to True for this model
        self.is_lecturer = True
        self.is_invigilator = True
        self.user_type = User.ACADEMIC_STAFF
        super(Lecturer, self).save(*args, **kwargs)
    
    def get_lecturer_schedule(self):
        # Logic to fetch and return the lecturer's teaching schedule
        # Example: Return all exams where the lecturer is involved as a course instructor
        pass
        # return Exam.objects.filter(course__lecturer=self)

    def get_invigilator_schedule(self):
        # Logic to fetch and return the invigilator schedule
        # Example: Return all exams where the lecturer is an invigilator
        pass
        # return Exam.objects.filter(invigilator=self)

class Student(User):
    class Meta:
        proxy = True
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
    def save(self, *args, **kwargs):
        # Ensure that the user type is set to Student
        self.user_type = User.STUDENT
        super(Student, self).save(*args, **kwargs)