from django.conf import settings
from django.views.generic import (
    TemplateView
)


class HomeView(TemplateView):

    template_name = 'management/home/home.html'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        IS_DEBUG = settings.DEBUG
        context.update({'IS_DEBUG': IS_DEBUG,
                        })
        return context