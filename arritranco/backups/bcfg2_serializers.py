# -*- coding: utf-8 -*-
from rest_framework import serializers
from backups.models import FileBackupTask
from inventory.models import PhysicalMachine

class Bcfg2BackupPropertySerializer(serializers.ModelSerializer):
    """Serialize backup properties for bcfg2."""

    minutes = serializers.Field(source='minute')
    hours = serializers.Field(source='hour')
    doms = serializers.Field(source='monthday')
    months = serializers.Field(source='month')
    dows = serializers.Field(source='weekday')
    extra = serializers.SerializerMethodField('get_extra')

    class Meta:
        model = FileBackupTask
        exclude = ('checker_fqdn',
                'minute',
                'hour',
                'monthday',
                'month',
                'weekday',
                'active',
                'duration',
                'extra_options',
                'bckp_type',
                'days_in_hard_drive',
                'max_backup_month',
                'machine',
                'active',
                'duration',)

    def get_extra(self,obj):
        data = {}
        if obj.extra_options:
            for l in obj.extra_options.split('\n'):
                pieces = l.split('=', 2)
                if len(pieces) > 1:
                    data[pieces[0]] = pieces[1]
        return data


class Bcfg2UPSPropertySerializer(serializers.ModelSerializer):
    """Serialize physical machine with epo_level."""

    class Meta:
        model = PhysicalMachine
