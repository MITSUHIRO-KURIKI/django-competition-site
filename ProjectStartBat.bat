@rem makemigrations の実行
python manage.py makemigrations contenttypes
python manage.py makemigrations auth
python manage.py makemigrations accounts
python manage.py makemigrations user_profile
python manage.py makemigrations user_settings
python manage.py makemigrations competitions
python manage.py makemigrations submission
python manage.py makemigrations discussions_and_notebooks
python manage.py makemigrations comments
python manage.py makemigrations bookmark
python manage.py makemigrations vote
python manage.py makemigrations user_inquiry
python manage.py makemigrations templatetags
python manage.py makemigrations admin
python manage.py makemigrations axes
python manage.py makemigrations django_summernote
python manage.py makemigrations sessions
python manage.py makemigrations default
python manage.py makemigrations social_auth
python manage.py makemigrations social_django
python manage.py makemigrations thumbnail
python manage.py makemigrations

@rem migrate の実行
python manage.py migrate contenttypes
python manage.py migrate auth
python manage.py migrate accounts
python manage.py migrate user_profile
python manage.py migrate user_settings
python manage.py migrate competitions
python manage.py migrate submission
python manage.py migrate discussions_and_notebooks
python manage.py migrate comments
python manage.py migrate bookmark
python manage.py migrate vote
python manage.py migrate user_inquiry
python manage.py migrate templatetags
python manage.py migrate admin
python manage.py migrate axes
python manage.py migrate django_summernote
python manage.py migrate sessions
python manage.py migrate default
python manage.py migrate social_auth
python manage.py migrate social_django
python manage.py migrate thumbnail
python manage.py migrate

@rem createsuperuser の実行
python manage.py createsuperuser

@rem runserver の実行
@REM python manage.py runserver