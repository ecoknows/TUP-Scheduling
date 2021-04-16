from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import (
    Subjects,
    CourseCurriculum,
    Professors,
    Students
)

from wagtail.core import hooks


class SubjectsAdmin(ModelAdmin):
    model = Subjects
    menu_label = 'Subjects'
    list_display = ('subject_code', 'description',
                    'units', 'lab_or_lec', 'sem', 'hours')
    list_filter = ('units', 'lab_or_lec', 'sem', 'hours')
    search_fields = ('subject_code', 'description',
                     'units', 'lab_or_lec', 'sem', 'hours')


class CourseCurriculumAdmin(ModelAdmin):
    model = CourseCurriculum
    menu_label = 'Course Curriculum'
    list_display = ('course_name', 'course_date')
    search_fields = ('course_name', 'course_date')
    list_filter = ('course_date',)


class AdminGroup(ModelAdminGroup):
    menu_label = 'Admin'
    menu_icon = 'user'
    menu_order = 100
    items = (SubjectsAdmin, CourseCurriculumAdmin)


modeladmin_register(AdminGroup)


class StudentsAdmin(ModelAdmin):
    model = Students
    menu_label = 'Students'
    # list_display = ('name', 'preferred_time', 'regular_or_part_time', 'department')
    # list_filter = ('name',)
    # search_fields = ('name', )


class ProfessorsAdmin(ModelAdmin):
    model = Professors
    menu_label = 'Professors'
    list_display = ('last_name', 'preferred_start_time', 'preferred_end_time',
                    'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'middle_name', 'last_name', )


class UsersGroup(ModelAdminGroup):
    menu_label = 'User'
    menu_icon = 'user'
    menu_order = 100
    items = (StudentsAdmin, ProfessorsAdmin)


modeladmin_register(UsersGroup)
