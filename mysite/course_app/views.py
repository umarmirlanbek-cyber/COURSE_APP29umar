from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from tokenize import TokenError

from .models import (
    UserProfile, Teacher, Category, SubCategory, Language,
    Course, Student, Chapter, Lesson, Assignment,
    Exam, Question, Option, Certificate, Review, ReviewLike, StudentNetwork
)
from .serializers import (
    UserProfileSerializer, UserProfileListSerializer, UserProfileDetailSerializer,
    TeacherSerializer, CategorySerializer, SubCategorySerializer, LanguageSerializer,
    CourseListSerializer, CourseDetailSerializer, ChapterSerializer, LessonSerializer,
    AssignmentSerializer, ExamSerializer, QuestionSerializer, OptionSerializer,
    CertificateSerializer, ReviewSerializer, ReviewListSerializer, StudentSerializer,
)
from .pagination import CoursePagination
from .permissions import StudentPermission, TeacherPermission
from .filters import CourseFilter


# ─── Auth ──────────────────────────────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh токен не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'detail': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)



class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class TeacherListAPIView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetailAPIView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer



class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer



class LanguageListAPIView(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer



class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CourseFilter
    ordering_fields = ['price']
    search_fields = ['course_name']
    pagination_class = CoursePagination


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [TeacherPermission]


class CourseUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [TeacherPermission]

    def get_queryset(self):
        return Course.objects.filter(created_by=self.request.user)



class ChapterListAPIView(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class ChapterDetailAPIView(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class ChapterCreateAPIView(generics.CreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [TeacherPermission]


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [TeacherPermission]


class AssignmentListAPIView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AssignmentCreateAPIView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [TeacherPermission]



class ExamListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class ExamDetailAPIView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class ExamCreateAPIView(generics.CreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [TeacherPermission]


class QuestionCreateAPIView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [TeacherPermission]


class OptionCreateAPIView(generics.CreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [TeacherPermission]



class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [StudentPermission]


class ReviewUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [StudentPermission]

    def get_queryset(self):
        return Review.objects.filter(student__user=self.request.user)



class CertificateListAPIView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class StudentDetailAPIView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [StudentPermission]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)