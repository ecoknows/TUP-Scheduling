
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from TUPScheduling.accounts.models import (
    Students,
    Professors,
)

from TUPScheduling import StringResources
from TUPScheduling.accounts.views import ProfessorCreateView, StudentCreateView

class Students(ModelAdmin):
    model = Students
    create_view_class = StudentCreateView
    menu_label = 'Students'
    list_display = ('first_name', 'section')
    list_filter = ('first_name', 'section')
    search_fields = ('first_name', 'section')

class Professors(ModelAdmin):
    model = Professors
    create_view_class = ProfessorCreateView
    menu_label = 'Professors'
    list_display = ('full_name', 'preferred_time', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'middle_name', 'last_name', 'full_name',)


class AccountsGroup(ModelAdminGroup):
    menu_label = 'Accounts'
    menu_icon = 'user'
    menu_order = 100
    items = (Students, Professors)


modeladmin_register(AccountsGroup)