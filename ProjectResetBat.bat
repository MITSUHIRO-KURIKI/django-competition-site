echo off
@rem ER図 の作成
python manage.py graph_models -a -g -o ERD.png
@rem データベースの削除
del db.sqlite3

@rem config の削除
rd /s /q config\__pycache__
rd /s /q config\extra_settings\__pycache__
rd /s /q config\views\__pycache__

@rem accounts の削除
rd /s /q accounts\__pycache__
rd /s /q accounts\migrations
rd /s /q accounts\forms\__pycache__
rd /s /q accounts\models\__pycache__
rd /s /q accounts\views\__pycache__

@rem user_profile の削除
rd /s /q user_profile\__pycache__
rd /s /q user_profile\migrations
rd /s /q user_profile\forms\__pycache__
rd /s /q user_profile\models\__pycache__
rd /s /q user_profile\views\__pycache__

@rem user_settings の削除
rd /s /q user_settings\__pycache__
rd /s /q user_settings\migrations
rd /s /q user_settings\forms\__pycache__
rd /s /q user_settings\models\__pycache__
rd /s /q user_settings\views\__pycache__

@rem templatetags の削除
rd /s /q templatetags\__pycache__
rd /s /q templatetags\migrations
rd /s /q templatetags\forms\__pycache__
rd /s /q templatetags\models\__pycache__
rd /s /q templatetags\views\__pycache__
rd /s /q templatetags\common\__pycache__
rd /s /q templatetags\competitions\__pycache__
rd /s /q templatetags\user_profile\__pycache__
rd /s /q templatetags\vote\__pycache__

@rem competitions の削除
rd /s /q competitions\__pycache__
rd /s /q competitions\migrations
rd /s /q competitions\forms\__pycache__
rd /s /q competitions\models\__pycache__
rd /s /q competitions\views\__pycache__

@rem submission の削除
rd /s /q submission\__pycache__
rd /s /q submission\migrations
rd /s /q submission\forms\__pycache__
rd /s /q submission\models\__pycache__
rd /s /q submission\views\__pycache__
rd /s /q submission\evaluation\__pycache__

@rem discussions_and_notebooks の削除
rd /s /q discussions_and_notebooks\__pycache__
rd /s /q discussions_and_notebooks\migrations
rd /s /q discussions_and_notebooks\forms\__pycache__
rd /s /q discussions_and_notebooks\forms\Discussions\__pycache__
rd /s /q discussions_and_notebooks\forms\Notebooks\__pycache__
rd /s /q discussions_and_notebooks\models\__pycache__
rd /s /q discussions_and_notebooks\views\__pycache__
rd /s /q discussions_and_notebooks\views\Discussions\__pycache__
rd /s /q discussions_and_notebooks\views\Notebooks\__pycache__
rd /s /q discussions_and_notebooks\Convert\__pycache__

@rem comments の削除
rd /s /q comments\__pycache__
rd /s /q comments\migrations
rd /s /q comments\forms\__pycache__
rd /s /q comments\models\__pycache__
rd /s /q comments\views\__pycache__
rd /s /q comments\Convert\__pycache__

@rem bookmark の削除
rd /s /q bookmark\__pycache__
rd /s /q bookmark\migrations
rd /s /q bookmark\forms\__pycache__
rd /s /q bookmark\models\__pycache__
rd /s /q bookmark\views\__pycache__

@rem vote の削除
rd /s /q vote\__pycache__
rd /s /q vote\migrations
rd /s /q vote\forms\__pycache__
rd /s /q vote\models\__pycache__
rd /s /q vote\views\__pycache__

@rem user_inquiry の削除
rd /s /q user_inquiry\__pycache__
rd /s /q user_inquiry\migrations
rd /s /q user_inquiry\forms\__pycache__
rd /s /q user_inquiry\models\__pycache__
rd /s /q user_inquiry\views\__pycache__

@rem management の削除
rd /s /q management\__pycache__
rd /s /q management\migrations
rd /s /q management\forms\__pycache__
rd /s /q management\models\__pycache__
rd /s /q management\views\__pycache__

@rem common_scripts の削除
rd /s /q common_scripts\__pycache__
rd /s /q common_scripts\migrations
rd /s /q common_scripts\forms\__pycache__
rd /s /q common_scripts\models\__pycache__
rd /s /q common_scripts\views\__pycache__

@rem media\cache の削除
rd /s /q media\cache

@rem media\django-summernote の削除
rd /s /q media\django-summernote

@rem media\user_profile\user_icon の削除
pushd media\user_profile\user_icon
for %%f in ( * ) do call :sub "%%f"
for /D %%f in ( * ) do call :sub "%%f" d
popd

@rem media\competitions\overall の削除
pushd media\competitions\overall
for %%f in ( * ) do call :sub "%%f"
for /D %%f in ( * ) do call :sub "%%f" d
popd

@rem media\competitions\data_file の削除
pushd media\competitions\data_file
for %%f in ( * ) do call :sub "%%f"
for /D %%f in ( * ) do call :sub "%%f" d
popd

@rem media\competitions\answer の削除
pushd media\competitions\answer
for %%f in ( * ) do call :sub "%%f"
for /D %%f in ( * ) do call :sub "%%f" d
popd

@rem media\submission の削除
pushd media\submission
for %%f in ( * ) do call :sub "%%f"
for /D %%f in ( * ) do call :sub "%%f" d
popd

@rem media\discussions_and_notebooks\notebooks の削除
pushd media\discussions_and_notebooks\notebooks
for %%f in ( * ) do call :sub "%%f"
for /D %%f in ( * ) do call :sub "%%f" d
popd

@rem media\discussions_and_notebooks\image の削除
pushd media\discussions_and_notebooks\image
for %%f in ( * ) do call :sub "%%f"
for /D %%f in ( * ) do call :sub "%%f" d
popd


@rem requirements.txt の作成
@REM conda list -e > conda_requirements.txt
@REM pip freeze > requirements.txt

exit /b
:sub
set flag=OFF
for %%e in ( default ) do if %1=="%%e" set flag=ON
if "%flag%"=="ON" goto :EOF
if "%2"=="" del %1
if "%2"=="d" rd /S /Q %1
goto :EOF