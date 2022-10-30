from django.conf import settings
from pathlib import os
from pathlib import Path
from competitions.models import (
    Competitions,
)
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import FileResponse
from django.http import Http404

class CompetitionDataFileView(View, LoginRequiredMixin):
    
    def get(self, request, *args, **kwargs):
        
        instance_id = self.kwargs['instance_id']
        competition = get_object_or_404(Competitions, id=instance_id)
        date_open = competition.date_open

        if self.request.user.is_superuser or self.request.user.is_staff:
            file_url = str(competition.data_file)
            filename = file_url.split('/')[-1]
            file_url = Path(file_url)
            root = settings.MEDIA_ROOT
            file_path = Path(str(root) +'/'+ str(file_url))
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)
        elif self.request.user.is_authenticated and competition.is_public and date_open < timezone.now():
            file_url = str(competition.data_file)
            filename = file_url.split('/')[-1]
            file_url = Path(file_url)
            root = settings.MEDIA_ROOT
            file_path = Path(str(root) +'/'+ str(file_url))
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)
        else:
            raise Http404