from .models import (
    Category, SubCategory, Language, Course,
    Chapter, Lesson, Assignment, Exam, Question, Option
)
from modeltranslation.translator import TranslationOptions, register


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('subcategory_name',)


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ('language_name',)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('course_name', 'description')


@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('chapter_name',)


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Assignment)
class AssignmentTranslationOptions(TranslationOptions):
    fields = ('assignment_name', 'description')


@register(Exam)
class ExamTranslationOptions(TranslationOptions):
    fields = ('exam_name',)


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ()


@register(Option)
class OptionTranslationOptions(TranslationOptions):
    fields = ('option_name',)