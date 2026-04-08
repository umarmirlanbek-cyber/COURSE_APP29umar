from django.urls import include, path
from rest_framework.routers import DefaultRouter,SimpleRouter
from .views import *

router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('teachers/', TeacherListAPIView.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/', TeacherDetailAPIView.as_view(), name='teacher_detail'),
    path('categories/', CategoryListAPIView.as_view(), name='category_list'),
    path('subcategories/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('languages/', LanguageListAPIView.as_view(), name='language_list'),
    path('courses/', CourseListAPIView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail'),
    path('courses/create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course_update'),
    path('chapters/', ChapterListAPIView.as_view(), name='chapter_list'),
    path('chapters/<int:pk>/', ChapterDetailAPIView.as_view(), name='chapter_detail'),
    path('chapters/create/', ChapterCreateAPIView.as_view(), name='chapter_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_detail'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('assignments/', AssignmentListAPIView.as_view(), name='assignment_list'),
    path('assignments/create/', AssignmentCreateAPIView.as_view(), name='assignment_create'),
    path('exams/', ExamListAPIView.as_view(), name='exam_list'),
    path('exams/<int:pk>/', ExamDetailAPIView.as_view(), name='exam_detail'),
    path('exams/create/', ExamCreateAPIView.as_view(), name='exam_create'),
    path('questions/create/', QuestionCreateAPIView.as_view(), name='question_create'),
    path('options/create/', OptionCreateAPIView.as_view(), name='option_create'),
    path('reviews/', ReviewListAPIView.as_view(), name='review_list'),
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewUpdateAPIView.as_view(), name='review_update'),
    path('certificates/', CertificateListAPIView.as_view(), name='certificate_list'),
    path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='student_detail'),
]