from django.conf import settings
from user_inquiry.models import (
    UserInquiry,
)
from django.views.generic import (
    ListView, DetailView,
    DeleteView,
)


class InquiryListView(ListView):

    model = UserInquiry
    template_name = 'management/inquiry/inquiry_list.html'
    context_object_name = "INQUIRY_DATA"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        IS_DEBUG = settings.DEBUG
        context.update({'IS_DEBUG': IS_DEBUG,
                        })
        return context