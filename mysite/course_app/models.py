from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import TextField, BooleanField
from phonenumber_field.formfields import PhoneNumberField


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'student'),
        ('teacher', 'teacher'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(17), MaxValueValidator(100)], null=True, blank=True)
    avatar = models.ImageField(upload_to='image_user', null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True)


class Teacher(UserProfile):
    phone_number = PhoneNumberField()


class NetworkTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='networks')
    network_name = models.CharField(max_length=32)
    network_url = models.URLField()


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.subcategory_name


class Language(models.Model):
    language_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.language_name


class Course(models.Model):
    choices_level = (
        ('начальный', 'начальный'),
        ('средний', 'средний'),
        ('продвинутый', 'продвинутый'),
    )
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    subcategory = models.ManyToManyField(SubCategory, related_name='courses')
    level = models.CharField(choices=choices_level, max_length=20, default='начальный')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    created_date = models.DateField(auto_now_add=True)
    update_at = models.DateField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='courses')
    course_image = models.ImageField(upload_to='image_course/')
    is_certificate = models.BooleanField()

    def __str__(self):
        return self.course_name


class Student(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='students')
    course = models.ManyToManyField(Course, related_name='students')


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')


class Lesson(models.Model):
    title = models.CharField(max_length=64)
    lesson_file = models.FileField(upload_to='lesson_files/', null=True, blank=True)
    content = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    has_assignment = models.BooleanField(default=True)


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=64)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField(verbose_name='deadline')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments')


class Exam(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='exams')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_name = models.CharField(max_length=32)
    duration = models.DurationField()


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_name = models.CharField(max_length=64)
    option_type = models.BooleanField()


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_file = models.FileField(upload_to='certificate_file/')
    created_date = models.DateField(auto_now_add=True)


class Review(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)


class ReviewLike(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='review_likes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)


class StudentNetwork(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='networks')
    network_name = models.CharField(max_length=32)
    network_url = models.URLField()