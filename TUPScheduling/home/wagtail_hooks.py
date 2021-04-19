from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import (
    Subjects,
    CourseCurriculum,
    Professors,
    Sections,
    Rooms,
    Departments,
    Colleges,

    StudentsAccount,
    ProfessorsAccount,
    AdminsAccount,

    SectionsSchedule,
    ProfessorsSchedule,
    RoomsSchedule,
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


class ProfessorsAdmin(ModelAdmin):
    model = Professors
    menu_label = 'Professors'
    list_display = ('full_name', 'preferred_time', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'middle_name', 'last_name', 'full_name',)


class SectionsAdmin(ModelAdmin):
    model = Sections
    menu_label = 'Sections'
    # list_display =
    # list_filter =
    # search_fields =


class RoomsAdmin(ModelAdmin):
    model = Rooms
    menu_label = 'Rooms'
    # list_display =
    # list_filter =
    # search_fields =


class DepartmentsAdmin(ModelAdmin):
    model = Departments
    menu_label = 'Departments'
    # list_display =
    # list_filter =
    # search_fields =


class CollegesAdmin(ModelAdmin):
    model = Colleges
    menu_label = 'Colleges'
    list_display = ('college_name',)
    list_filter = ('college_name',)
    search_fields = ('college_name',)


class AdminGroup(ModelAdminGroup):
    menu_label = 'Admin'
    menu_icon = 'user'
    menu_order = 100
    items = (SubjectsAdmin, CourseCurriculumAdmin, ProfessorsAdmin,
             SectionsAdmin, RoomsAdmin, DepartmentsAdmin, CollegesAdmin)


modeladmin_register(AdminGroup)


class StudentsAccount(ModelAdmin):
    model = StudentsAccount
    menu_label = 'Students'
    # list_display =
    # list_filter =
    # search_fields =


class ProfessorsAccount(ModelAdmin):
    model = ProfessorsAccount
    menu_label = 'Professors'
    # list_display =
    # list_filter =
    # search_fields =


class AdminsAccount(ModelAdmin):
    model = AdminsAccount
    menu_label = 'Admins'
    # list_display =
    # list_filter =
    # search_fields =


class AccountsGroup(ModelAdminGroup):
    menu_label = 'Accounts'
    menu_icon = 'user'
    menu_order = 100
    items = (StudentsAccount, ProfessorsAccount, AdminsAccount)


modeladmin_register(AccountsGroup)


class SectionsSchedule(ModelAdmin):
    model = SectionsSchedule
    menu_label = 'Sections'
    # list_display =
    # list_filter =
    # search_fields =


class ProfessorsSchedule(ModelAdmin):
    model = ProfessorsSchedule
    menu_label = 'Professors'
    # list_display =
    # list_filter =
    # search_fields =


class RoomsSchedule(ModelAdmin):
    model = RoomsSchedule
    menu_label = 'Rooms'
    # list_display =
    # list_filter =
    # search_fields =


class SchedulesGroup(ModelAdminGroup):
    menu_label = 'Schedules'
    menu_icon = 'user'
    menu_order = 100
    items = (SectionsSchedule, ProfessorsSchedule, RoomsSchedule)


modeladmin_register(SchedulesGroup)
