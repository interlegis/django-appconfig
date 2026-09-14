from django.urls import path
from . import views

app_name = "appconfig"

urlpatterns = [
    path("appconfig/", views.configlist, name="appconfiglist"),
    path("appconfig/<str:appname>/", views.configform, name="appconfigform"),
]
