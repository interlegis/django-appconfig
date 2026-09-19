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

from appconfig.appconfig import App
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
    app_list = config.get_apps()
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
        app = App(appname)
    except Exception as e:
        raise Http404(str(e))

    if request.method == "POST":
        form = app.configform_class(
            data=request.POST,
            files=request.FILES,
            initial=app.get_fields(),
        )
        if form.is_valid():
            app.update_fields(form.cleaned_data)
            app.save()
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
        form = app.configform_class(initial=app.get_fields())

    title = (
        form.form_title
        if hasattr(form, "form_title")
        else _("{appname} settings").format(appname=appname)
    )
    subtitle = form.form_subtitle if hasattr(form, "form_subtitle") else None

    return render(
        request,
        "appconfig/configform.html",
        context={
            "title": title,
            "subtitle": subtitle,
            "form": form,
            "app": app,
        },
    )
