from django.conf import settings
from django.db import models
from sorl.thumbnail import get_thumbnail, delete
from django.core.files.base import ContentFile

# Notebookの画像を一時保存する先(Notebookの画像を別途保存する場合に使用する)
def get_dummy_image_path(instance, filename):
    return f'discussions_and_notebooks/image/{instance.notebook.id}/{filename}'

class DummyImageUpload(models.Model):

    dummy_name = models.CharField(verbose_name='NotebookImage_name', max_length=10, blank=False, null=False,)
    dummy_image = models.ImageField(verbose_name='NotebookImage_image', upload_to=get_dummy_image_path,
                                    blank=True, null=True,)
    notebook = models.ForeignKey(to='NotebookThemes', on_delete=models.CASCADE,
                                 related_name='related_dummy_image_upload_notebook',)

    def save(self, *args, **kwargs):

        # data_file処理(upload_to に instance.id を使うため)
        data_file_process = False
        if self.id is None: # instance.id がないとき(初回登録時発火)
            data_file_process = True
            dummy_image_ = self.dummy_image
            self.dummy_image = None # 一旦 Null で保存
        
        super(DummyImageUpload, self).save(*args, **kwargs) # 一度保存(data_file処理以外でも共通)

        if data_file_process:
            self.dummy_image = dummy_image_
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
            super(DummyImageUpload, self).save(*args, **kwargs)

        try:
            resize_width = settings.NOTEBOOK_IMAGE_WIDTH
            resize_height = settings.NOTEBOOK_IMAGE_HEIGHT
            if self.dummy_image.width > resize_width or self.dummy_image.height > resize_height:
                new_width = resize_width
                new_height = resize_height

                resized = get_thumbnail(self.dummy_image, "{}x{}".format(new_width, new_height))
                name = self.dummy_image.name.split('/')[-1]
                self.dummy_image.save(name, ContentFile(resized.read()), True)
                delete(resized) # キャッシュファイルの削除
        except: pass # dummy_image が無い場合には処理回避

    class Meta:
        db_table = 'dummy_image_upload_model'
        verbose_name=verbose_name_plural='NotebookImageUpload'