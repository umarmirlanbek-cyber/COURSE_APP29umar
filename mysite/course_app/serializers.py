from rest_framework import serializers
from .models import (
    UserProfile, Teacher, NetworkTeacher, Category, SubCategory,
    Language, Course, Student, Chapter, Lesson, Assignment,
    Exam, Question, Option, Certificate, Review, ReviewLike, StudentNetwork
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'role']


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'role', 'date_registered']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'bio', 'avatar']


class NetworkTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkTeacher
        fields = ['network_name', 'network_url']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name', 'category']


class SubCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language_name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    student = UserProfileSerializer(source='student.user')
    created_date = serializers.DateField(format='%Y-%m-%d')
    class Meta:
        model = Review
        fields = ['id', 'student', 'text', 'rating', 'created_date']


class CourseListSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    subcategory = SubCategoryNameSerializer()
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_image', 'price', 'level',
                  'language', 'subcategory']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'has_assignment']


class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_name', 'lessons']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_name', 'option_type']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True, source='option_set')
    class Meta:
        model = Question
        fields = ['id', 'score', 'options']


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')
    class Meta:
        model = Exam
        fields = ['id', 'exam_name', 'duration', 'questions']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'course', 'certificate_file', 'created_date']


class CourseDetailSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    subcategory = SubCategorySerializer()
    created_by = TeacherSerializer()
    chapters = ChapterSerializer(many=True, read_only=True, source='chapter_set')
    reviews = ReviewListSerializer(many=True, read_only=True, source='review_set')
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_image', 'description', 'price', 'level',
                  'language', 'subcategory', 'created_by', 'created_date', 'is_certificate',
                  'chapters', 'reviews']



class StudentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    courses = CourseListSerializer(many=True, read_only=True, source='course')
    class Meta:
        model = Student
        fields = ['id', 'user', 'courses']