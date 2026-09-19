from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Config(models.Model):
    app_name = models.CharField(_("app name"), max_length=100)
    field_name = models.CharField(_("field name"), max_length=100)
    field_value = models.BinaryField(
        _("binary field value"),
    )

    class Meta:
        ordering = ("app_name", "field_name")
        verbose_name = _("Config parameter")
        verbose_name_plural = _("Config parameters")

    def __str__(self):
        return f"{self.app_name}.{self.field_name}: {self.field_value}"
