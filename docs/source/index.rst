.. Django Appconfig documentation master file, created by
   sphinx-quickstart on Thu Sep 10 12:01:46 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Appconfig documentation
==============================

A helper to manage user settings per app in your Django projects.

Sometimes, developing transactional business applications, we need to persist
some data that has no relationship with the models of the system,
like an email address to send alerts, or a list of URLs to scrap in a cronjob.

Normally, this type of data is usually kept in the `settings.py` project
file. But if this data changes with a moderate or hight frequency, we need
redeploy the project whenever a change is made.

There is also data that needs to be persisted for use at different stages of a process lifecycle, such as the date of the last execution or a hash of data fetched from the web.

An alternative is to write a Model to persist these data in the database, but
this type of model has no one relationship with other models in project, they
appear to be "floating" in a class diagram.

To avoid this awkwardness, the Django appconfig manages your app config data
and persists it in a single model ``appconfig.Config``, giving you a simple
way to access these data in your code.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   how_to_use
   templates
   api

