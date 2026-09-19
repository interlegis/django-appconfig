API Reference
=============

.. module:: appconfig
   :synopsis: Appconfig classes and methods

AppConfig
---------

.. class:: appconfig.appconfig.AppConfig

   The main class for accessing applications with configuration settings. You do not need to instantiate this class directly; instead, use the global ``config`` object, which is a pre-built instance of this class.

   **Methods**

   .. method:: getapps()

      Returns a list of :class:`App` objects for all installed apps that contain a valid ``appconfig`` module.

   **Attributes**

   This class has no static attributes. Instead, you can access :class:`App` objects dynamically using the app name as an attribute (e.g., ``config.myapp``).


App
---

.. class:: appconfig.appconfig.App(app_name)

   Represents an application that defines an ``AppConfigForm`` class within its ``appconfig.py`` module. This object is used to manage your app's settings.

   Instantiate it by passing the name of the target app, for example::

      myapp = App('myapp')

   **Methods**

   .. method:: get_fields()

      Returns a dictionary containing all setup fields and their respective values.

      :rtype: dict

   .. method:: update_fields(field_data)

      Updates the field values using the provided dictionary. This change is local to the object and is not immediately persisted to the database.

      :param dict field_data: A dictionary containing the fields and their new values.

   .. method:: remove_field(fieldname)

      Removes a field from the object and deletes its corresponding record from the database.

      :param str fieldname: The name of the field to be removed.

   .. method:: save()

      Persists all fields defined in the object to the database.

   **Attributes**

   .. attribute:: appname

      *Read-only*. A string representing the name of the application that the object instantiates.

   .. attribute:: appconfig

      *Read-only*. The :class:`django.apps.config.AppConfig` descendant object associated with the Django app.

   .. attribute:: configform_class

      The ``AppConfigForm`` class fetched from the application's configuration form.

   .. note::
      All application configuration fields can be accessed directly as attributes of the :class:`App` instance.
