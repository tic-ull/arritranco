'''
Created 08/03/2012

@author: alorenzo
'''
from django.contrib import admin
from models import NagiosCheck, NagiosCheckOpts, NagiosContactGroup


class NagiosCheckOptsInline(admin.TabularInline):
    model = NagiosCheckOpts

class NagiosCheckAdmin(admin.ModelAdmin):
    prepopulated_fields = { "slug": ("name",)}
    list_display = ('name', 'default', 'default_params')
    filter_horizontal = ('machines',)
    list_editable = ('default',)
    search_fields = ('name',)
    inlines = [NagiosCheckOptsInline,]


class NagiosCheckOptsAdmin(admin.ModelAdmin):
    list_display = ('check','machine','options')
    list_editable = ('options',)
    search_fields = ('check__name','machine_fqdn')

class NagiosContactGroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(NagiosCheckOpts, NagiosCheckOptsAdmin)
admin.site.register(NagiosCheck, NagiosCheckAdmin)
admin.site.register(NagiosContactGroup)
