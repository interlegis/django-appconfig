Templates
=========

Django-appconfig uses two templates that extend `admin/base_site.html` to render the settings menu and the forms:

appconfig/configlist.html
-------------------------

Renders the app settings menu. This template receives the following context variables:

* `applist`: A list of all apps that have a appconfig.AppconfigForm class defined.
* `title`: the translation string ``_("App configuration")``

appconfig/configform.html
-------------------------

Renders the app config form, with the following context variables:

  * `form`: The AppconfigForm instance to be rendered
  * `title`: The translation string `_("{appname} settings")`

Overriding these templates
--------------------------

If you need customize these templates, you can override them in your main project template diretory or in any template directory inside your installed apps. See `How to override templates <https://docs.djangoproject.com/en/6.1/howto/overriding-templates/>`_ in Django.
