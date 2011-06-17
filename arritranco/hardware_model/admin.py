from django.contrib import admin

from models import Manufacturer, HwModel, HwType

admin.site.register(Manufacturer)
admin.site.register(HwModel)
admin.site.register(HwType)