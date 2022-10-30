from django.contrib import admin
from user_settings.models import(
    CustomUserMailSettings, CustomUserProfilePublicSettings,
)


class CustomUserMailSettingsAdmin(admin.ModelAdmin):

    # 紐付いている外部のテーブルを参照
    def External_Reference_is_active(self, obj):
        return obj.user.is_active
    External_Reference_is_active.short_description = 'user__is_active'

    list_display_ = ('user',
                     'email_receipt_permission_all',
                     'email_receipt_permission_important_notice',
                     'email_receipt_user_competition_notice',
                     'email_receipt_user_discussion_comment_notice',
                     'email_receipt_user_notebook_comment_notice',
                     'External_Reference_is_active',
                     )
    list_display = list_display_
    list_display_links = list_display_

    # ユーザ作成画面 表示項目
    add_fieldsets = (
        ('ユーザ (OntToOneField CustomUser.email)', {'fields': (
            'user',
            )}),
        ('ユーザ許諾情報_メール受信(一般)', {'fields': (
            'email_receipt_permission_all',
            'email_receipt_permission_important_notice',
            )}),
        ('ユーザ許諾情報_メール受信(通知)', {'fields': (
            'email_receipt_user_competition_notice',
            'email_receipt_user_discussion_comment_notice',
            'email_receipt_user_notebook_comment_notice',
            )}),
    )

    # ユーザ編集画面 表示項目
    fieldsets = (
        ('ユーザ (OntToOneField CustomUser.email)', {'fields': (
            'user',
            )}),
        ('ユーザ許諾情報_メール受信', {'fields': (
            'email_receipt_permission_all',
            'email_receipt_permission_important_notice',
            )}),
        ('ユーザ許諾情報_メール受信(通知)', {'fields': (
            'email_receipt_user_competition_notice',
            'email_receipt_user_discussion_comment_notice',
            'email_receipt_user_notebook_comment_notice',
            )}),
    )

    list_filter = ['user',
                   'email_receipt_permission_all',
                   'email_receipt_permission_important_notice',
                   'email_receipt_user_competition_notice',
                   'email_receipt_user_discussion_comment_notice',
                   'email_receipt_user_notebook_comment_notice',
                   'user__is_active']
    search_fields = ('user__email',
                     'user__username',
                     )
    ordering = ('pk',)

class CustomUserProfilePublicSettingsAdmin(admin.ModelAdmin):

    # 紐付いている外部のテーブルを参照
    def External_Reference_is_active(self, obj):
        return obj.user.is_active
    External_Reference_is_active.short_description = 'user__is_active'

    list_display_ = ('user',
                     'user_profile_is_authenticated_only',
                     'user_profile_is_all_public',
                     'search_robot_public',
                     'username_public',
                     'user_icon_public',
                     'locate_public',
                     'birth_day_public',
                     'gender_public',
                     'sns_id_public',
                     'External_Reference_is_active',
                     )
    list_display = list_display_
    list_display_links = list_display_

    # ユーザ作成画面 表示項目
    add_fieldsets = (
        ('ユーザ (OntToOneField CustomUser.email)', {'fields': (
            'user',
            )}),
        ('ユーザプロフィール公開設定_一般', {'fields': (
            'user_profile_is_authenticated_only',
            'user_profile_is_all_public',
            'search_robot_public',
        )}),
        ('ユーザプロフィール公開設定_項目', {'fields': (
            'username_public',
            'comment_public',
            'user_icon_public',
            'locate_public',
            'birth_day_public',
            'gender_public',
            'sns_id_public',
        )}),
    )

    # ユーザ編集画面 表示項目
    fieldsets = (
        ('ユーザ (OntToOneField CustomUser.email)', {'fields': (
            'user',
            )}),
        ('ユーザプロフィール公開設定_一般', {'fields': (
            'user_profile_is_authenticated_only',
            'user_profile_is_all_public',
            'search_robot_public',
        )}),
        ('ユーザプロフィール公開設定_項目', {'fields': (
            'username_public',
            'comment_public',
            'user_icon_public',
            'locate_public',
            'birth_day_public',
            'gender_public',
            'sns_id_public',
        )}),
    )

    list_filter = ['user',
                   'user_profile_is_authenticated_only',
                   'user_profile_is_all_public',
                   'search_robot_public',
                   'username_public',
                   'comment_public',
                   'user_icon_public',
                   'locate_public',
                   'birth_day_public',
                   'gender_public',
                   'sns_id_public',
                   'user__is_active',
                   ]
    search_fields = ('user__email',
                     'user__username',
                     )
    ordering = ('pk',)

admin.site.register(CustomUserMailSettings, CustomUserMailSettingsAdmin)
admin.site.register(CustomUserProfilePublicSettings, CustomUserProfilePublicSettingsAdmin)