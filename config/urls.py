from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from config.views import (
    HomeView,
)
from competitions.views import(
    CompetitionDataFileView,
)
from submission.views import (
    UserSubmissionFileView, 
)

urlpatterns = [
    path('admin/', admin.site.urls, ),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('competitions/', include('competitions.urls')),
    path('submission/', include('submission.urls')),
    path('discussions/', include('discussions_and_notebooks.discussions_urls')),
    path('notebooks/', include('discussions_and_notebooks.notebooks_urls')),
    path('comments/', include('comments.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('vote/', include('vote.urls')),
    path('user_inquiry/', include('user_inquiry.urls')),
    path('management/', include('management.urls')),
    path('privacy/', TemplateView.as_view(template_name='common/privacy.html'), name='privacy'),
    path('disclaimer/', TemplateView.as_view(template_name='common/disclaimer.html'), name='disclaimer'),
    path('auth/', include('social_django.urls', namespace='social')), # ADD social-auth-app-django
    path('summernote/', include('django_summernote.urls')), # ADD django-summernote
]
# competition answer file の秘匿
if not settings.USE_GCS:
    urlpatterns += path('media/competitions/answer/<int:instance_id>/<str:filename>', TemplateView.as_view(template_name='home/home.html'), name='competition_answer_file'),
# submission file の秘匿
if not settings.USE_GCS:
    urlpatterns += path('media/submission/<str:unique_competition_id>/<int:user_id>/<int:instance_id>/<str:filename>', UserSubmissionFileView.as_view(), name='user_submission_file'),
# competition data file の秘匿
if not settings.USE_GCS:
    urlpatterns += path('media/competitions/data_file/<int:instance_id>/<str:filename>', CompetitionDataFileView.as_view(), name='competition_data_file'),

# runserver で 静的/メディア ファイルを配信するための設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# USE django-toolbar
if settings.USE_DJANGO_TOOLBAR:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]