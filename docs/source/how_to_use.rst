How to use
==========

:synopsis: How to use the django-appconfig

Writing a form
--------------

In your app's directory, create a file named `appconfig.py` and implement a class named `AppconfigForm` that inherits from `django.forms.Form`. Then, define the fields you wish to persist for this app. Use the `initial` parameter for each field to set its default values.

e.g:

.. code-block:: python

    from django import forms

    class AppConfigForm(forms.Form):
        email = forms.EmailField(
            label="E-mail",
            help_text="E-mail address to send scrap resume report",
            required=True,
        )
        urls = forms.CharField(
            label="URLs to scrap",
            help_text="Add one URL per line",
            required=True,
            widget=forms.Textarea,
        )


Note: The filename `appconfig.py` and the class name `AppconfigForm` are mandatory and must be typed exactly as shown.

Setting values in admin interface
---------------------------------

Access your system's administrative interface and navigate to the URL `/admin/appconfig/` to view a list of apps that have an AppConfigForm defined.

Click any link to edit the settings for that app.

Note that the default django-admin dashboard does not expose the `/admin/appconfig/` URL. You must provide this in your project.

Retrieving app settings in your code
------------------------------------

To retrieve user settings for your apps, use the `config` object provided by the django-appconfig package:

.. code-block:: python

    from appconfig import config
    ...
    value = config.<appname>.<fieldname>


Replace <appname> and <fieldname> with the name of the app and the config field you wish to access.
