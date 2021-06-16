from django.contrib.auth.models import Group

from wagtail.contrib.modeladmin.views import CreateView

from TUPScheduling.users.models import User


class ProfessorCreateView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()
        

        user = User.objects.create_user(
            username=instance.user_code(extra_count=5000),
            first_name=instance.first_name,
            last_name=instance.last_name,
            password=instance.last_name.upper(),
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
            password=instance.last_name.upper(),
            email=instance.first_name + '.' + instance.last_name + '@tup.edu.ph',
        )
        
        instance.user = user

        group = Group.objects.get(name='Student')
        group.user_set.add(user)


        return super().form_valid(form)
