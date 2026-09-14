from datetime import datetime
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from . import (
    config,
    APPCONFIG_UPLOAD_PATH_DEFAULT,
    APPCONFIG_CAN_CONFIG_DEFAULT,
)
from .models import Config


@user_passes_test(
    getattr(settings, "APPCONFIG_CAN_CONFIG", APPCONFIG_CAN_CONFIG_DEFAULT)
)
def configlist(request):
    app_list = config.get_app_configs()
    return render(
        request,
        "appconfig/configlist.html",
        context={"applist": app_list, "title": _("App configuration")},
    )


@user_passes_test(
    getattr(settings, "APPCONFIG_CAN_CONFIG", APPCONFIG_CAN_CONFIG_DEFAULT)
)
def configform(request, appname):
    try:
        ConfigForm = config.get_configform_class(appname)
    except config.AppConfigFormDoesNotExists:
        raise Http404(
            _("Config form not found to app {appname}").format(appname=appname)
        )
    if request.method == "POST":
        form = ConfigForm(
            data=request.POST,
            files=request.FILES,
            initial=getattr(config, appname).__dict__,
        )
        # prepare_file_fields(form)
        if form.is_valid():
            # Save form values and files
            for field_name, field_value in form.cleaned_data.items():
                if isinstance(field_value, UploadedFile):
                    file_name = (
                        Path(
                            getattr(
                                settings,
                                "APPCONFIG_UPLOAD_PATH",
                                APPCONFIG_UPLOAD_PATH_DEFAULT,
                            ).format(
                                appname=appname,
                                fieldname=field_name,
                                datetime=datetime.now(),
                            )
                        )
                        / field_value.name
                    )
                    db_value = default_storage.save(file_name, field_value)
                else:
                    db_value = str(field_value)

                Config.objects.update_or_create(
                    app_name=appname,
                    field_name=field_name,
                    defaults={"field_value": db_value},
                )
            messages.add_message(
                request,
                messages.SUCCESS,
                _("{appname} settings saved successfully").format(
                    appname=appname
                ),
            )
            if "_continue" not in request.POST:
                return redirect("appconfig:appconfiglist")
    else:
        form = ConfigForm(initial=getattr(config, appname).__dict__)
        # prepare_file_fields(form)
    return render(
        request,
        "appconfig/configform.html",
        context={
            "title": _("{appname} settings").format(appname=appname),
            "form": form,
        },
    )
