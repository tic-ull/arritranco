# -*- coding: utf-8 -*-
from rest_framework import serializers
from scheduler.models import Task, TaskCheck, TaskStatus
from django.conf import settings

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ('check_time', 'status', 'comment')

class TaskCheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskCheck

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
