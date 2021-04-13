from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Subjects, CourseCurriculum

from wagtail.core import hooks

class SubjectsAdmin(ModelAdmin):
	model = Subjects
	menu_label = 'Subjects'
	list_display = ('subject_code', 'description', 'units', 'lab_or_lec', 'sem', 'hours')
	list_filter = ('units','lab_or_lec', 'sem', 'hours')
	search_fields = ('subject_code', 'description', 'units', 'lab_or_lec', 'sem', 'hours')

class CourseCurriculumAdmin(ModelAdmin):
	model = CourseCurriculum
	menu_label = 'Course Curriculum'
	list_display = ('course_name', 'course_date')
	search_fields = ('course_name', 'course_date')
	list_filter = ('course_date',)

class AdminGroup(ModelAdminGroup):
	menu_label = 'Admin'
	menu_icon = 'user'
	menu_order = 000
	items = (SubjectsAdmin, CourseCurriculumAdmin)

modeladmin_register(AdminGroup)

