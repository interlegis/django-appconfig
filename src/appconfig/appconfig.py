import importlib
from pathlib import Path
from django import forms
from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _


class App:
    """Represents an application configuration

    Args:
        app_name (str): the app name
        parameters (dict): A dictionary with all appconfig parameters
    """

    app_name = ""

    def __init__(self, app_name, parameters):
        self.app_name = app_name
        self.__dict__.update(parameters)


class AppConfig:
    """A class what retrieve all app configs"""

    class AppConfigFormDoesNotExists(Exception):
        pass

    def get_configform_class(self, app):
        """Get the AppConfigForm class from app

        Args:
            app (AppconfigConfig | str): An appconfig.apps.AppconfigConfig
                                         object or an app name

        Raises:
            self.AppConfigFormDoesNotExists: If the app does not have
                                             AppConfigForm class

        Returns:
            AppConfigForm class
        """
        if isinstance(app, str):
            # carregar o app
            try:
                app = apps.get_app_config(app)
            except LookupError:
                raise self.AppConfigFormDoesNotExists(
                    _("Has no app with name {appname}").format(appname=app)
                )
        # Buscar a classe AppconfigForm no módulo "appconfig" na app
        try:
            app_config = importlib.import_module(".appconfig", package=app.name)
        except ModuleNotFoundError:
            raise self.AppConfigFormDoesNotExists(
                _("App {app_name} does not have appconfig module").format(
                    app_name=app.name
                )
            )
        if not hasattr(app_config, "AppConfigForm"):
            raise self.AppConfigFormDoesNotExists(
                _(
                    "App {app_name} does not have AppConfigForm class in its "
                    "appconfig module"
                ).format(app_name=app.name)
            )
        AppConfigForm = getattr(app_config, "AppConfigForm")
        if not issubclass(AppConfigForm, forms.Form):
            raise self.AppConfigFormDoesNotExists(
                _(
                    "The AppConfigForm of {app_name} is not a "
                    "django.form.Form subclass"
                ).format(app_name=app.name)
            )

        return AppConfigForm

    def __getattr__(self, attrname):
        from .models import Config

        # Get AppConfigForm class in attrname app
        try:
            AppConfigForm = self.get_configform_class(attrname)
        except self.AppConfigFormDoesNotExists as e:
            raise AttributeError(str(e))

        # Creates a dict with all form fields and loads its values from
        # database, or from field 'initial' property if no database
        # value is found

        data_dict = dict()

        for field_name in AppConfigForm.base_fields:
            dbrec = Config.objects.filter(
                app_name=attrname, field_name=field_name
            ).first()
            if dbrec:
                if isinstance(
                    AppConfigForm.base_fields[field_name], forms.FileField
                ):
                    file_name = dbrec.field_value
                    file = default_storage.open(file_name)
                    file.name = file_name
                    file.url = default_storage.url(file_name)
                    data_dict[field_name] = file
                else:
                    data_dict[field_name] = dbrec.field_value
            else:
                data_dict[field_name] = AppConfigForm.base_fields[
                    field_name
                ].initial

        # Instantiates the ConfigForm, put the data_dict as data in the form
        # instance to validade and converts into python native values.

        form = AppConfigForm(data=data_dict)
        if form.is_valid():
            data_dict = form.cleaned_data

        # Transforma o dicionário obtido em um objeto App

        app_obj = App(attrname, data_dict)

        return app_obj

    def get_app_configs(self):
        """Returns a list of AppconfigConfig of apps that have a valid
           appconfig module

        Returns:
            list: A list of django.apps.AppconfigConfig
        """
        app_list = []
        for app in apps.get_app_configs():
            # Get AppConfigForm class in attrname app
            try:
                AppConfigForm = self.get_configform_class(app)
            except self.AppConfigFormDoesNotExists as e:
                continue
            app_list.append(app)
        return app_list
