from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from accounts.models import(
    UserActivateTokens,
)
from accounts.forms import(
    AdminCustomUserCreationForm,
)


User = get_user_model()

class CustomUserAdmin(UserAdmin): 

    add_form = AdminCustomUserCreationForm # ユーザ作成画面のForm
    
    # ユーザ一覧画面 表示項目
    list_display_ = ('email', 'unique_account_id', 'is_active', 'is_social_login', 'is_set_password', 'is_staff','date_joined',)
    list_display = list_display_
    list_display_links = list_display_

    # ユーザ作成画面 表示項目
    add_fieldsets = (
        ('ユーザ情報', {'fields': (
            'email', 'unique_account_id', 'password', 'confirm_password',
            )}),
    )

    # ユーザ編集画面 表示項目
    fieldsets = (
        ('ユーザ情報', {'fields': (
            'email', 'unique_account_id', 'username', 'password',
            )}),
        ('権限', {'fields': (
            'is_active', 'is_social_login', 'is_set_password', 'change_email_on_request', 'is_staff', 'is_superuser',
            )}),
    )

    list_filter = ['email', 'date_joined', 'is_active',]
    search_fields = ('email', 'unique_account_id', 'username',)
    ordering = ('pk',)


class UserActivateTokensAdmin(admin.ModelAdmin):

    # 紐付いている外部のテーブルを参照
    def External_Reference_is_active(self, obj):
        return obj.user.is_active
    External_Reference_is_active.short_description = 'user__is_active'
    
    # ユーザ一覧画面 表示項目
    list_display_ = ('user', 'expired_at', 'External_Reference_is_active')
    list_display = list_display_
    list_display_links = list_display_

    list_filter = ['user__is_active', 'expired_at']
    search_fields = ('user__email',
                     'user__username'
                    )
    ordering = ('user__is_active',)


admin.site.register(User,  CustomUserAdmin)
admin.site.register(UserActivateTokens, UserActivateTokensAdmin)

admin.site.unregister(Group) # AdminSite GROUR unregister