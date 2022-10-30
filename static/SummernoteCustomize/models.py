from django.db import models
from django_summernote.utils import get_attachment_storage, get_attachment_upload_to

# 画像のリサイズ用にカスタマイズ ここから 1/3
from django.conf import settings
from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail, delete
# 画像のリサイズ用にカスタマイズ ここまで 1/3

__all__ = ['AbstractAttachment', 'Attachment', ]


class AbstractAttachment(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Defaults to filename, if left blank")

# 画像のリサイズ用にカスタマイズ ここから 2/3
#    file = models.FileField( # セキュリティ上画像ファイルのアップロードには ImageField を使う
    file = models.ImageField(
# 画像のリサイズ用にカスタマイズ ここまで 2/3
        upload_to=get_attachment_upload_to(),
        storage=get_attachment_storage()
    )
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
# 画像のリサイズ用にカスタマイズ ここから 3/3
#        super().save(*args, **kwargs)
        super(AbstractAttachment, self).save(*args, **kwargs)
        try:
            resize_width = settings.SUMMERNOTE_IMAGE_WIDTH
            if self.file.width > resize_width:
                new_width = resize_width
                new_height = int(self.file.height*(resize_width/self.file.width))

                resized = get_thumbnail(self.file, "{}x{}".format(new_width, new_height))
                name = self.file.name.split('/')[-1]
                print(name )
                self.file.save(name, ContentFile(resized.read()), True)
                delete(resized) # キャッシュファイルの削除
        except: pass # user_icon が無い場合には処理回避
# 画像のリサイズ用にカスタマイズ ここまで 3/3

    class Meta:
        abstract = True


class Attachment(AbstractAttachment):
    pass
