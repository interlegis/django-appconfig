import base64
import importlib
import pickle
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from django import forms
from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _


class AppConfigFormDoesNotExists(Exception):
    pass


@dataclass
class AppconfigFile:
    name: str


class App:
    """Represents an application configuration"""

    _appname = ""
    _djangoappconfig = None
    _appconfigformclass = None
    _appconfigform = None

    def __init__(self, appname):
        self._appname = appname
        self.__dict__.update(self.get_fields())

    def __getattr__(self, name):
        from .models import Config

        # Try get value from database
        try:
            record = Config.objects.get(app_name=self._appname, field_name=name)
            value_b64 = record.field_value
        except Config.DoesNotExist:
            # Try get default value from form
            form = self.configform_class()
            if name in form.fields:
                value_b64 = base64.b64encode(
                    pickle.dumps(form.fields[name].initial)
                )
            else:
                value_b64 = base64.b64encode(pickle.dumps(None))
        value = pickle.loads(base64.b64decode(value_b64))
        setattr(self, name, value)
        return value

    def __get_configform_class__(self):
        app = self.appconfig
        # Buscar a classe AppconfigForm no módulo "appconfig" na app
        try:
            appconfig_module = importlib.import_module(
                ".appconfig", package=app.name
            )
        except ModuleNotFoundError:
            raise AppConfigFormDoesNotExists(
                _("App {app_name} does not have appconfig module").format(
                    app_name=self._appname
                )
            )
        if not hasattr(appconfig_module, "AppConfigForm"):
            raise AppConfigFormDoesNotExists(
                _(
                    "App {app_name} does not have AppConfigForm class in its "
                    "appconfig module"
                ).format(app_name=self._appname)
            )
        AppConfigForm = getattr(appconfig_module, "AppConfigForm")
        if not issubclass(AppConfigForm, forms.Form):
            raise AppConfigFormDoesNotExists(
                _(
                    "The AppConfigForm of {app_name} is not a "
                    "django.form.Form subclass"
                ).format(app_name=self._appname)
            )
        return AppConfigForm

    @property
    def appname(self):
        return self._appname

    @property
    def appconfig(self):
        if not self._djangoappconfig:
            self._djangoappconfig = apps.get_app_config(self._appname)
        return self._djangoappconfig

    @property
    def configform_class(self):
        if not self._appconfigformclass:
            self._appconfigformclass = self.__get_configform_class__()
        return self._appconfigformclass

    def get_fields(self):
        from .models import Config

        fields = dict()

        # Get form initial values
        form = self.configform_class()
        for fieldname, field in form.fields.items():
            fields[fieldname] = field.initial
            if isinstance(field, forms.FileField) and field.initial is not None:
                # default_storage.open(file_name)
                fields[fieldname] = File(
                    field.initial.name, open(field.initial.name, "rb")
                )
                fields[fieldname].url = field.initial.url

        # Get database data (override initial if necessary)
        for record in Config.objects.filter(app_name=self._appname):
            value = pickle.loads(base64.b64decode(record.field_value))
            if isinstance(value, AppconfigFile):
                file = default_storage.open(value.name)
                file.name = value.name
                file.url = default_storage.url(value.name)
                value = file
            fields[record.field_name] = value
        # Update with object values
        for fieldname, fieldvalue in self.__dict__.items():
            if not fieldname.startswith("_"):
                fields[fieldname] = fieldvalue
        return fields

    def update_fields(self, field_data):
        from . import APPCONFIG_UPLOAD_PATH_DEFAULT

        for fieldname, fieldvalue in field_data.items():
            if isinstance(fieldvalue, UploadedFile):
                filename = (
                    Path(
                        getattr(
                            settings,
                            "APPCONFIG_UPLOAD_PATH",
                            APPCONFIG_UPLOAD_PATH_DEFAULT,
                        ).format(
                            appname=self.appname,
                            fieldname=fieldname,
                            datetime=datetime.now(),
                        )
                    )
                    / fieldvalue.name
                )
                filename = default_storage.save(filename, fieldvalue)
                value = default_storage.open(filename)
                value.name = filename
                value.url = default_storage.url(filename)
            else:
                value = fieldvalue
            setattr(self, fieldname, value)

    def remove_field(self, fieldname):
        if not hasattr(self, fieldname):
            raise AttributeError(f"Field {fieldname} does not exists")
        value = getattr(self, fieldname)
        from .models import Config

        Config.objects.filter(
            app_name=self._appname, field_name=fieldname
        ).delete()
        delattr(self, fieldname)
        return value

    def save(self):
        from .models import Config

        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if isinstance(value, File):
                    value = AppconfigFile(value.name)
                value_b64 = base64.b64encode(pickle.dumps(value))
                Config.objects.update_or_create(
                    app_name=self._appname,
                    field_name=key,
                    defaults={"field_value": value_b64},
                )


class AppConfig:
    """A class what retrieve all app configs"""

    def __getattr__(self, attrname):
        try:
            app = App(attrname)
        except:
            raise AttributeError(f"'AppConfig' has no attribute '{attrname}' ")
        self.__dict__[attrname] = app
        return app

    def get_apps(self):
        """List of App objects for all installed apps that have a
        valid appconfig module

        Returns:
            list: A list of django.apps.AppconfigConfig
        """
        app_list = []
        for app in apps.get_app_configs():
            try:
                app = App(app.label)
            except:
                continue
            app_list.append(app)
        return app_list
