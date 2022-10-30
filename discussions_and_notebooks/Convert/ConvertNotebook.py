from django.conf import settings
from nbconvert import ( 
    HTMLExporter,
)
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from uuid import uuid4
import base64
import copy
import gc
from google.cloud import storage
from io import BytesIO

if settings.NOTEBOOK_IMAGE_UPLOAD:
    import os
    import shutil
    from discussions_and_notebooks.models.DummyImage_models import (
        DummyImageUpload,
    )


def notebook2html(notebook_file_path):

    html_exporter = HTMLExporter()
    if settings.USE_GCS:
        gcs = storage.Client()
        client = gcs.from_service_account_json(settings.GS_CREDENTIALS_JSON)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(notebook_file_path)
        html, _ = html_exporter.from_file(BytesIO(blob.download_as_string()))
    else:
        html, _ = html_exporter.from_filename(notebook_file_path)

    soup = BeautifulSoup(html, "html.parser")
    
    file_name = soup.find("title").text

    html_style = soup.find_all("style")
    html_style = "".join(map(str,html_style))
    
    html_body = soup.find("body").contents
    html_body = "".join(map(str,html_body))

    del html_exporter, html, soup
    gc.collect()

    return file_name, html_style, html_body

if settings.NOTEBOOK_IMAGE_UPLOAD:
    # 埋め込み画像をアップロードする場合に使用
    def embedding_notebook_images(notebook_instance, html_body):

        # アップロード前に画像があれば一旦すべて削除
        # try:
        #     if settings.USE_GCS:
        #         file_folder = os.path.join(settings.STATIC_URL.split('/')[-1], 'discussions_and_notebooks', 'image', f'{notebook_instance.id}')
        #     else:
        #         file_folder = os.path.join(settings.MEDIA_ROOT, 'discussions_and_notebooks', 'image', f'{notebook_instance.id}')
        #     shutil.rmtree(file_folder+'/')
        #     os.mkdir(file_folder+'/')
        # except: pass

        soup = BeautifulSoup(html_body, "html.parser")

        image_byte = None
        image_obj = None
        for img_tag in soup.find_all('img'):
            try:
                name = str(uuid4())[:10]
                self_model = DummyImageUpload.objects.get_or_create(dummy_name=name, notebook=notebook_instance)

                # instance.id の発行のため一度 save()
                self_model.save()

                img_tag_ = copy.copy(img_tag)
                image_b64 = img_tag_.get('src').split('base64,')[1]
                image_type = img_tag_.get('src').split('data:image/')[1].split(';')[0]
                img_name = name+'.'+image_type
                
                image_byte = base64.b64decode(image_b64)
                image_obj = ContentFile(image_byte)

                # image file の保存
                self_model.dummy_image.save(img_name, image_obj)

                # save した画像の url で置き換え
                img_tag_.attrs['src'] = self_model.dummy_image.url
                soup = str(soup).replace(str(img_tag),str(img_tag_))
            except: pass


        del image_byte, image_obj
        gc.collect()

        html_body = str(soup)
        return html_body


def notebook_convert(notebook_instance, notebook_file_path):

    file_name, html_style, html_body = notebook2html(notebook_file_path)

    if settings.NOTEBOOK_IMAGE_UPLOAD:
        html_body = embedding_notebook_images(notebook_instance, html_body)

    return file_name, html_style, html_body