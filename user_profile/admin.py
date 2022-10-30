from django.contrib import admin
from user_profile.models import(
    CustomUserProfile,
)
from django.utils.safestring import mark_safe
from datetime import  date


class CustomUserProfileAdmin(admin.ModelAdmin):

    # ユーザ一覧画面 表示項目
    # ユーザアイコンの表示
    def user_icon_preview(self, obj):
        try:
             return mark_safe(f'<img src="{obj.user_icon.url}" style="width:25px;height:25px;">')
        except: pass
    user_icon_preview.short_description = 'ユーザアイコン'

    # 生年月日から年齢の表示
    def age_preview(self, obj):
        if obj.birth_day is None:
            return 0
        else:
            today = date.today()
            return today.year - obj.birth_day.year - ((today.month, today.day) < (obj.birth_day.month, obj.birth_day.day))
    age_preview.short_description = '年齢'

    # 紐付いている外部のテーブルを参照
    def External_Reference_date_joined(self, obj):
        return obj.user.date_joined.strftime('%Y/%m/%d')
    External_Reference_date_joined.short_description = 'user__date_joined'

    def External_Reference_is_active(self, obj):
        return obj.user.is_active
    External_Reference_is_active.short_description = 'user__is_active'
    
    list_display_ = ('user',
                     'user_icon_preview',
                     'locate',
                     'birth_day',
                     'age_preview',
                     'gender',
                     'External_Reference_date_joined',
                     'External_Reference_is_active',
                     )
    list_display = list_display_
    list_display_links = list_display_

    # ユーザ作成画面 表示項目
    add_fieldsets = (
        ('ユーザ (OntToOneField CustomUser.email)', {'fields': (
            'user',
            )}),
        ('ユーザ追加情報_一般', {'fields': (
            'user_icon',
            'comment',
            'locate',
            'birth_day',
            'gender',
            )}),
        ('ユーザ追加情報_SNS', {'fields': (
            'sns_id_twitter',
            'sns_id_facebook',
            'sns_id_instagram',
            'sns_id_linkedin',
            'sns_id_github',
            'sns_id_kaggle',
            )}),
    )

    # ユーザ編集画面 表示項目
    fieldsets = (
        ('ユーザ (OntToOneField CustomUser.email)', {'fields': (
            'user',
            )}),
        ('ユーザ追加情報_一般', {'fields': (
            'user_icon',
            'comment',
            'locate',
            'birth_day',
            'gender',
            )}),
        ('ユーザ追加情報_SNS', {'fields': (
            'sns_id_twitter',
            'sns_id_facebook',
            'sns_id_instagram',
            'sns_id_linkedin',
            'sns_id_github',
            'sns_id_kaggle',
            )}),
    )

    list_filter = ['user',
                   'user__date_joined',
                   'user__is_active',
                   ]
    search_fields = ('user__email',
                     'user__username',
                     'comment',
                     'sns_id_twitter',
                     'sns_id_facebook',
                     'sns_id_instagram',
                     'sns_id_linkedin',
                     'sns_id_github',
                     'sns_id_kaggle',
                     )
    ordering = ('pk',)


admin.site.register(CustomUserProfile, CustomUserProfileAdmin)