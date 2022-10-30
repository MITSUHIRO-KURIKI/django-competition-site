import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import re
import itertools
from bs4 import BeautifulSoup
import copy

User = get_user_model()

def clean_space_tag(text):
    text = text.replace('&nbsp;',' ')
    return text

def correspondence_target(text):
    soup = BeautifulSoup(text, "html.parser")
    for link_tag in soup.find_all("a"):
        link_tag_ = copy.copy(link_tag)
        link_tag_.attrs['rel'] = 'noopener noreferrer'
        soup = str(soup).replace(str(link_tag),str(link_tag_))
    text = str(soup)
    return text

def comment2mention(text):

    # This should allow for better coding with hard coding!
    account_page_url = settings.FRONTEND_URL+'accounts/profile/'

    # comment2mention
    p = r'(\@\S*\ )'
    r = re.findall(p,text)
    # print(r)
    # print(len(r))
    if len(r) > 0:
        for mention in r:
            username = mention[1:-1]
            # print(mention+':mentionend')
            # print(username+':usernameend')
            try:
                user = get_object_or_404(User, username=username)
                unique_account_id = user.unique_account_id
                text=text.replace(mention,f'<a href="{account_page_url}{unique_account_id}">@{username}</a> ')
                # print(text+':textend')
            except:
                pass
    convert_text = text
    return convert_text

def convert_comment(text):
    # crean &nbsp;
    text = clean_space_tag(text)
    # target="_blank" Correspondence
    text = correspondence_target(text)
    # mention
    text = comment2mention(text)
    return text

def del_image(pre_text, post_text):
    # uploadしたが、投稿実行前に削除された画像は残ってしまう...

    # pre_text に含まれる image
    pre_image_list=[]
    soup = BeautifulSoup(pre_text, "html.parser")
    for img_tag in soup.find_all("img"):
        pre_image_list.append(img_tag.get('src'))

    # post_text に含まれる image
    post_image_list=[]
    soup = BeautifulSoup(post_text, "html.parser")
    for img_tag in soup.find_all("img"):
        post_image_list.append(img_tag.get('src'))
    
    # 削除された画像を特定
    pre_image_list = set(pre_image_list)
    post_image_list = set(post_image_list)
    del_image_path_list = pre_image_list - post_image_list

    if len(del_image_path_list) > 0:
        for img_path in del_image_path_list:
            # try:
            img_path_ = img_path.split('/')
            del_img_path = os.path.join(settings.MEDIA_ROOT, img_path_[-3], img_path_[-2], img_path_[-1])
            os.remove(del_img_path)
            # except: pass

    return 0