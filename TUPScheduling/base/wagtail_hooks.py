from django.http import request
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from TUPScheduling.base.models import (
    BulkSections,
    Subjects,
    CourseCurriculum,
    Sections,
    Rooms,
    Departments,
    Colleges,
)

from TUPScheduling.schedule.models import (
    SectionsSchedule,
    ProfessorsSchedule,
    RoomsSchedule,
)

from wagtail.core import hooks
from django.utils.html import format_html
from django.templatetags.static import static

@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/admin.css"))


class SubjectsAdmin(ModelAdmin):
    model = Subjects
    menu_label = 'Subjects'
    list_display = ('subject_code', 'description',
                    'units', 'lab_or_lec', 'hours')
    list_filter = ('units', 'lab_or_lec', 'hours')
    search_fields = ('subject_code', 'description',
                     'units', 'lab_or_lec', 'hours')


class CourseCurriculumAdmin(ModelAdmin):
    model = CourseCurriculum
    menu_label = 'Course Curriculum'
    list_display = ('course_name', 'department',
                    'curriculum_year')
    search_fields = ('course_name', 'college__college_name',
                     'department__Department_Name', 'curriculum_year')
    list_filter = ('department', 'curriculum_year')


class SectionsAdmin(ModelAdmin):
    index_template_name = 'sections.html'

    model = Sections
    menu_label = 'Sections'
    list_display = (
        'section_name',
        'year_level',
        'sem',
        'course_curriculum',
        'department',
    )
    list_filter = (
        'year_level',
        'sem',
        'course_curriculum',
        'department',
    )
    search_fields = (
        'section_name',
        'year_level',
        'sem',
        'course_curriculum__course_name',
        'college__college_name',
        'department__Department_Name',
    )


class BulkSectionsAdmin(ModelAdmin):
    model = BulkSections
    menu_label = 'Bulk Section'
    list_display = (
        'course_curriculum__course_name',
    )
    list_filter = (
        'course_curriculum__course_name',
    )
    search_fields = (
        'course_curriculum__course_name',
    )


modeladmin_register(BulkSectionsAdmin)


class RoomsAdmin(ModelAdmin):
    model = Rooms
    menu_label = 'Rooms'
    list_display = (
        'Room_Name',
        'Room_Type',
    )
    list_filter = (
        'Room_Type',
    )
    search_fields = (
        'Room_Name',
        'Room_Type',
    )


class DepartmentsAdmin(ModelAdmin):
    model = Departments
    menu_label = 'Departments'

    list_display = (
        'Department_Name',
        'Choose_College',
    )
    list_filter = (
        'Choose_College',
    )
    search_fields = (
        'Department_Name',
        'Choose_College',
    )


class CollegesAdmin(ModelAdmin):
    index_template_name = 'colleges.html'
    model = Colleges
    menu_label = 'Colleges'
    list_display = ('college_name',)
    search_fields = ('college_name',)
    list_export = ('college_name',)


class AdminGroup(ModelAdminGroup):
    menu_label = 'Admin'
    menu_icon = 'user'
    menu_order = 100
    items = (
        SubjectsAdmin,
        CourseCurriculumAdmin,
        SectionsAdmin,
        RoomsAdmin,
        DepartmentsAdmin,
        CollegesAdmin
    )


modeladmin_register(AdminGroup)

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


@hooks.register("construct_main_menu")
def hide_workflows(request, menu_items):
    menu_items[:] = [
        item for item in menu_items if item.name != "bulk-section"]
