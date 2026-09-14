Installation instructions
=========================

:synopsis: Installing Django-appconfig in your project

Installing
----------

You can use ``pip`` to install Django-appconfig for usage:

  $ pip install -e git+https://github.com/interlegis/django-appconfig.git#egg=django-appconfig


Configuration
-------------

To enable `Django-appconfig` in your project you need to add ``appconfig`` to ``INSTALLED_APPS`` in your project's ``settings.py`` file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'appconfig',
    )

Run ``python manage.py migrate`` to create django-appconfig database tables.

Edit your project's ``url.py`` file and include `appconfig.urls` in your urlpatterns:

.. code-block:: python

    from django.urls import path, include

    urlpatterns = [
        ...
        path("admin/", include("appconfig.urls")),
        path("admin/", admin.site.urls),
        ...
    ]

Other settings
--------------

There are two other settings that can be added to your project's settings.py:

APPCONFIG_UPLOAD_PATH
^^^^^^^^^^^^^^^^^^^^^

default: **"appconfig/{appname}/{fieldname}"**

Specifies the path relative to MEDIA_ROOT where uploaded files will be saved. You can define three markplaces:

  * `{appname}`: replaced by the name of the app to which the files belong,
  * `{fieldname}`: replaced by the file-field name,
  * `{datetime}`: replaced by datetime.now() at the moment the file is saved.

APPCONFIG_CAN_CONFIG
^^^^^^^^^^^^^^^^^^^^

default: **lambda user: user.is_superuser**

Set this to a lambda expression that takes a User object and evaluates to ``True`` if the user can access the settings, or ``False`` if they cannot.

This lambda expression is used in the `@user_passes_test() <https://docs.djangoproject.com/en/6.1/topics/auth/default/#django.contrib.auth.decorators.user_passes_test>`_ decorator of the django-appconfig views.