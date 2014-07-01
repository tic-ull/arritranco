# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from backups.models import BackupFile, BackupTask, FileBackupProduct, FileBackupTask, TSMBackupTask, R1BackupTask
from django.conf import settings

import os


class BackupFileInfoSerializer(serializers.ModelSerializer):
    """Serializer for detail info about a backup file"""
    path = serializers.SerializerMethodField('get_full_path')

    class Meta:
        model = BackupFile
        fields = (
            'id',
            'path',
            'original_file_name',
            'original_date',
            'original_file_size',
            'original_md5',
            'compressed_file_name',
            'compressed_date',
            'compressed_file_size',
            'compressed_md5',
        )

    def get_full_path(self, obj):
        return os.path.join(obj.file_backup_product.file_backup_task.directory, obj.original_file_name)


class BackupFileSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField('get_full_path')

    class Meta:
        model = BackupFile
        fields = ('id', 'path', 'original_file_size', 'deletion_date', 'compressed_file_size')

    def get_full_path(self, obj):
        return os.path.join(obj.file_backup_product.file_backup_task.directory, obj.original_file_name)


class BackupFileToDeleteSerializer(serializers.ModelSerializer):
    """Serializer for te files to delete."""
    path = serializers.SerializerMethodField('get_full_path')
    pk = serializers.Field(source='id')

    class Meta:
        model = BackupFile
        fields = ('pk', 'path')

    def get_full_path(self, obj):
        return os.path.join(obj.file_backup_product.file_backup_task.directory,
                            obj.compressed_file_name or obj.original_file_name)


class FileBackupProductSerializer(serializers.ModelSerializer):
    pattern = serializers.SerializerMethodField('get_pattern')

    class Meta:
        model = FileBackupProduct
        #fields = ('start_seq', 'end_seq', 'variable_percentage')
        exclude = ('id', 'file_backup_task', 'file_pattern')

    def get_pattern(self, obj):
        return obj.file_pattern.pattern.strip()


class FileBackupTaskSerializer(serializers.ModelSerializer):
    checker = serializers.ChoiceField(source='checker_fqdn', choices=settings.FILE_BACKUP_CHECKERS)
    description = serializers.CharField()
    directory = serializers.CharField()
    files = FileBackupProductSerializer(source='file_backup', many=True)
    id = serializers.Field()
    last_run = serializers.DateTimeField(source='last_run')
    previous_run = serializers.SerializerMethodField('get_previous_run')
    next_run = serializers.DateTimeField('next_run')
    previous_run_files = serializers.SerializerMethodField('get_previous_run_files')

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
                   'machine',)

    def get_previous_run(self, obj):
        return obj.last_run(obj.last_run())

    def get_previous_run_files(self, obj):
        prev_run = obj.last_run(obj.last_run())

        try:
            tc = obj.taskcheck_set.get(task_time=prev_run)
            files = tc.backupfile_set.all()
            if files:
                return [BackupFileSerializer(x).data for x in files]
            else:
                return ''
        except ObjectDoesNotExist:
            return ''




class BackupTaskSerializer(serializers.ModelSerializer):
    nextrun = serializers.DateTimeField(source='next_run')

    class Meta:
        model = BackupTask
        fields = (
            'nextrun',
            'minute',
            'hour',
            'monthday',
            'month',
            'weekday',
            'active',
            'duration',
            'extra_options',
            'bckp_type',
            'machine',)

    def next_run(self, obj):
        return obj.next_run()


class HostTSMBackupTaskSerializer(serializers.ModelSerializer):
    """Serialize host info for a TSM task."""
    fqdn = serializers.SerializerMethodField('get_machine_fqdn')
    ipaddress = serializers.SerializerMethodField('get_ipaddress')

    class Meta:
        model = TSMBackupTask
        fields = ('fqdn', 'tsm_server', 'ipaddress')

    def get_machine_fqdn(self, obj):
        return obj.machine.fqdn

    def get_ipaddress(self, obj):
        return obj.machine.get_service_ip()


class R1BackupTaskSerializer(serializers.ModelSerializer):
    """Serialize tsm task info."""

    class Meta:
        model = R1BackupTask