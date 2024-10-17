from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator


class Department(models.Model):
    name = models.CharField(max_length=255)  # Department name
    email = models.EmailField(null=True, blank=True, unique=True)  # Nullable email
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
        # Construct the display name with prefix, first name, last name, and username (if available)
        parts = []

        if self.prefix:
            parts.append(self.prefix)
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)

        # Join the available parts with spaces
        display_name = ' '.join(parts)

        # If no meaningful name parts are available, just return the username
        if display_name:
            return f"{display_name} ({self.username})"
        else:
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

class Course(models.Model):
    code = models.CharField(max_length=15,
                            validators=[MinLengthValidator(2)])
    name = models.CharField(max_length=255, 
                            validators=[MinLengthValidator(2)])
    coordinator = models.ForeignKey('Lecturer', on_delete=models.SET_NULL, null=True, blank=True)
    department  = models.ForeignKey('Department', on_delete=models.CASCADE)


    def __str__(self):
        # Return a string combining the course code and name
        return f"{self.code} - {self.name}"

class Section(models.Model):
    number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(200)],
        help_text='Section or group number for the course '
    )
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        # Return a string combining course info and section number
        return f"{self.course.code} - {self.course.name} <S{self.number}>"

class Room(models.Model):
    # Room types
    CLASS_ROOM = 10
    COMPUTER_LAB = 20
    PHYSICS_LAB = 30
    CHEMISTRY_LAB = 40
    CAD_WORKSHOP = 50
    LECTURE_HALL = 60

    ROOM_TYPE_CHOICES = [
        (CLASS_ROOM, 'Classroom'),
        (COMPUTER_LAB, 'Computer Lab'),
        (PHYSICS_LAB, 'Physics Lab'),
        (CHEMISTRY_LAB, 'Chemistry Lab'),
        (CAD_WORKSHOP, 'CAD Workshop'),
        (LECTURE_HALL, 'Lecture Hall'),
    ]

    # Campuses
    SA = 'SA'
    AK = 'AK'

    CAMPUS_CHOICES = [
        (SA, 'Al Saada Campus'),
        (AK, 'Al Akhdar Campus')
    ]

        
    label = models.CharField(max_length=15, 
                             validators=[MinLengthValidator(2)])
    
    room_type = models.PositiveIntegerField(choices=ROOM_TYPE_CHOICES)

    campus = models.CharField(max_length=10,
                              validators=[MinLengthValidator(2)], choices=CAMPUS_CHOICES)
    
    capacity = models.PositiveBigIntegerField()

    block = models.CharField(max_length=15, validators=[MinLengthValidator(2)])

    class Meta:
        # Adding a unique constraint for the combination of label and campus
        constraints = [
            models.UniqueConstraint(fields=['label', 'campus'], name='unique_room_label_campus')
        ]

    def __str__(self):
        # Return the room label and campus in the desired format
        campus_name = dict(self.CAMPUS_CHOICES).get(self.campus, 'Unknown Campus')
        return f"{self.label} ({campus_name})"

   



