

from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from .models import (
    Students,
    Professors,
)

from TUPScheduling import StringResources

class Students(ModelAdmin):
    model = Students
    menu_label = 'Students'
    list_display = ('first_name', 'section')
    list_filter = ('first_name', 'section')
    search_fields = ('first_name', 'section')

class Professors(ModelAdmin):
    model = Professors
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