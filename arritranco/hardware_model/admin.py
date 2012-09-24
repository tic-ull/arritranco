from django.contrib import admin

from models import Manufacturer, HwModel, HwType, RackableModel
import logging
logger = logging.getLogger(__name__)

class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class HwModelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'manufacturer__name']
    list_display = ('name', 'manufacturer', 'type')
    list_filter = ('manufacturer', 'type')
    actions = ['convert_rackable_model', 'convert_rackable_model_2u', 'convert_rackable_model_4u']

    def convert_rackable_model(self, request, queryset, units = 1):
        for obj in queryset:
            #if not isinstance(obj, RackableModel):
            try:
                logger.debug('obj: %s already is a RackableModel', obj.rackablemodel)
            except RackableModel.DoesNotExist:
                logger.debug('Creating a RackableModel copy of %s with %s units', obj, units)
                rackable_version = RackableModel.objects.create(name = obj.name, slug = obj.slug, manufacturer = obj.manufacturer, type = obj.type, units = units)
                for hw in obj.hwbase_set.all():
                    logger.debug('Setting model for %s', hw)
                    hw.model = rackable_version
                    hw.save()
                logger.debug(u'Deleting %s', obj)
                obj.delete()
    convert_rackable_model.short_description = u"Convert model into 1 unit rackable model"

    def convert_rackable_model_2u(self, request, queryset):
        self.convert_rackable_model(request, queryset, 2)
    convert_rackable_model_2u.short_description = u"Convert model into 2 units rackable model"

    def convert_rackable_model_4u(self, request, queryset):
        self.convert_rackable_model(request, queryset, 4)
    convert_rackable_model_4u.short_description = u"Convert model into 4 units rackable model"

class RackableModelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'manufacturer__name', 'units']
    list_display = ('name', 'manufacturer', 'type', 'units')
    list_filter = ('manufacturer', 'units', 'type')

admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(HwModel, HwModelAdmin)
admin.site.register(HwType)
admin.site.register(RackableModel, RackableModelAdmin)
