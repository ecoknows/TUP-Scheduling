

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

from users.models import User
from django.contrib.auth.models import Group
from TUPScheduling import StringResources

class ProfessorsView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()
        
        user = User.objects.create_user(
            username=instance.user_code(),
            first_name= instance.first_name,
            last_name= instance.last_name,
            password=instance.last_name.upper(),
            professor=instance,
            email=instance.first_name + '.' + instance.last_name + '@tup.edu.ph',
        )

        
            
        group = Group.objects.get(name=self.model_admin.group_name)
        
        group.user_set.add(user)
        
        return super().form_valid(form)
        
class StudentsView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()
        
        user = User.objects.create_user(
            username=instance.user_code(),
            first_name= instance.first_name,
            last_name= instance.last_name,
            password=instance.last_name.upper(),
            student=instance,
            email=instance.first_name + '.' + instance.last_name + '@tup.edu.ph',
        )
            
        group = Group.objects.get(name=self.model_admin.group_name)
        
        group.user_set.add(user)
        
        return super().form_valid(form)
        
        
class Students(ModelAdmin):
    model = Students
    create_view_class = StudentsView
    menu_label = 'Students'
    group_name = StringResources.STUDENT
    list_display = ('first_name', 'section')
    list_filter = ('first_name', 'section')
    search_fields = ('first_name', 'section')

class Professors(ModelAdmin):
    model = Professors
    create_view_class = ProfessorsView
    menu_label = 'Professors'
    group_name = StringResources.PROFESSOR
    list_display = ('full_name', 'preferred_time', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'middle_name', 'last_name', 'full_name',)


class AccountsGroup(ModelAdminGroup):
    menu_label = 'Accounts'
    menu_icon = 'user'
    menu_order = 100
    items = (Students, Professors)


modeladmin_register(AccountsGroup)