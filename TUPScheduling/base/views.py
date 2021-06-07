
from wagtail.contrib.modeladmin.views import IndexView

class CollegeIndexView(IndexView):
    
    def get_context_data(self):
        print('Hello World')
        return super().get_context_data()