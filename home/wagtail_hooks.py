from django.http import request
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from wagtail.contrib.modeladmin.views import CreateView
from .models import (
    Subjects,
    CourseCurriculum,
    Sections,
    Rooms,
    Departments,
    Colleges,

)

from schedule.models import (
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


class ProfessorsAdmin(ModelAdmin):
    model = Professors
    menu_label = 'Professors'
    list_display = ('full_name', 'preferred_time', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'middle_name', 'last_name', 'full_name',)


class SectionView(CreateView):
    def sample(self):
        if 'test' in self.request.GET:
            return self.request.GET['test']
        else:
            return 0

    # def dispatch(self, request, *args, **kwargs):
    #     if self.is_pagemodel:
    #         user = request.user
    #         parents = self.permission_helper.get_valid_parent_pages(user)
    #         parent_count = parents.count()

    #         # There's only one available parent for this page type for this
    #         # user, so we send them along with that as the chosen parent page
    #         if parent_count == 1:
    #             parent = parents.get()
    #             parent_pk = quote(parent.pk)
    #             return redirect(self.url_helper.get_action_url(
    #                 'add', self.app_label, self.model_name, parent_pk))

    #         # The page can be added in multiple places, so redirect to the
    #         # choose_parent view so that the parent can be specified
    #         return redirect(self.url_helper.get_action_url('choose_parent'))
    #     return super().dispatch(request, *args, **kwargs)


class SectionsAdmin(ModelAdmin):
    create_template_name = 'bulk_section.html'
    index_template_name = 'sections.html'
    create_view_class = SectionView

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
        'section_name',
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


class RoomsAdmin(ModelAdmin):
    model = Rooms
    menu_label = 'Rooms'
    # list_display =
    # list_filter =
    # search_fields =


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
    model = Colleges
    menu_label = 'Colleges'
    list_display = ('college_name',)
    list_filter = ('college_name',)
    search_fields = ('college_name',)


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
