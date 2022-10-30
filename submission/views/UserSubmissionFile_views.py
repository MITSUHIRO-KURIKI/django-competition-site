from django.conf import settings
from pathlib import os
from pathlib import Path
from submission.models import (
    SubmissionUser,
)
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.http import Http404

class UserSubmissionFileView(View, LoginRequiredMixin):
    
    def get(self, request, *args, **kwargs):
        
        instance_id = self.kwargs['instance_id']
        submission = get_object_or_404(SubmissionUser, id=instance_id)

        if self.request.user.is_superuser or self.request.user.is_staff:
            file_url = str(submission.submission_file)
            filename = file_url.split('/')[-1]
            file_url = Path(file_url)
            root = settings.MEDIA_ROOT
            file_path = Path(str(root) +'/'+ str(file_url))
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)
        elif submission.join_user == self.request.user:
            file_url = str(submission.submission_file)
            filename = file_url.split('/')[-1]
            file_url = Path(file_url)
            root = settings.MEDIA_ROOT
            file_path = Path(str(root) +'/'+ str(file_url))
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)
        else:
            raise Http404