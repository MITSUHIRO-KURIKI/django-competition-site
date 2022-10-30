from django.contrib import admin
from user_inquiry.models import (
    UserInquiry,
)
from datetime import  date


class UserInquiryAdmin(admin.ModelAdmin):
    
    # 関連情報の有無
    def Reference_subject(self, obj):

        if obj.subject_comment:
            text='comment'
        elif obj.subject_discussion:
            text='discussion'
        elif obj.subject_notebook:
            text='notebook'
        else:
            text='None'
        return text
    Reference_subject.short_description = 'Reference_subject'


    list_display_ = ('inquirer_user',
                     'fixed_subject',
                     'Reference_subject',
                     'date_create',
                     'situation',
                     'date_complete',
                     )
    list_display = list_display_
    list_display_links = list_display_


    # 表示項目
    fieldsets = (
        ('問い合わせ者', {'fields': (
            'inquirer_user',
            'email',
            'date_create',
            )}),
        ('問い合わせ内容', {'fields': (
            'fixed_subject',
            'subject_text',
            )}),
        ('関連情報', {'fields': (
            'subject_comment',
            'subject_discussion',
            'subject_notebook',
            )}),
        ('対応状況', {'fields': (
            'situation',
            'date_complete',
            )}),
    )


    list_filter = ['fixed_subject',
                   'situation',
                   'date_create',
                   'date_complete',
                   ]
    search_fields = ('inquirer_user__email',
                     'inquirer_user__username',
                     'email',
                     'subject_text',
                     )
    ordering = ('situation','date_create',)


admin.site.register(UserInquiry, UserInquiryAdmin)