from django.contrib.auth.models import Group

from wagtail.contrib.modeladmin.views import CreateView, IndexView

from TUPScheduling.users.models import User
from django.http import HttpResponseRedirect
from TUPScheduling.schedule.models import Schedule
from TUPScheduling.accounts.models import Professors
from wagtail.admin import messages

def delete_schedule_of_professor(request,prof_pk):
    if request.user.is_superuser and prof_pk:
        Schedule.objects.filter(prof_id=prof_pk).delete()
        messages.success(
            request, 'You successfully deleted schedule of ' + Professors.objects.get(pk=prof_pk).last_name 
        )
    
    return HttpResponseRedirect('/admin/accounts/professors/')


class ProfessorCreateView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()
        

        user = User.objects.create_user(
            username=instance.user_code(extra_count=5000),
            first_name=instance.first_name,
            last_name=instance.last_name,
            password=instance.last_name.upper(),
            is_professor=True,
            email=instance.first_name + '.' + instance.last_name + '@tup.edu.ph',
        )
        
        instance.user = user

        group = Group.objects.get(name='Professor')
        group.user_set.add(user)


        return super().form_valid(form)


class StudentCreateView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()
        
        user = User.objects.create_user(
            username=instance.user_code(extra_count=3000),
            first_name=instance.first_name,
            last_name=instance.last_name,
            is_student=True,
            password=instance.last_name.upper(),
            email=instance.first_name + '.' + instance.last_name + '@tup.edu.ph',
        )
        
        instance.user = user

        group = Group.objects.get(name='Student')
        group.user_set.add(user)


        return super().form_valid(form)
