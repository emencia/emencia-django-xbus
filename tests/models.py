# -*- coding: utf-8 -*-
from django.db import models

from xbus.models import XbusAwareMixin


class EmitterWithoutMethod(XbusAwareMixin, models.Model):
    """To test emitter without method"""
    name = models.CharField(u'Titre', max_length=255)
    emitter = True


class SimpleEmitter(XbusAwareMixin, models.Model):
    """To test simple emitter"""
    name = models.CharField(u'Titre', max_length=255)
    emitter = True

    @staticmethod
    def get_xbus_event_type(event_type):
        """Get the event type"""
        return 'try_{event_type}'.format(event_type=event_type)

    def get_xbus_fields(self):
        fields = {'name': self.name}
        return fields

    def get_admin_url(self):
        """Get the admin url"""
        return ''


class EmitterWithExitCondition(XbusAwareMixin, models.Model):
    """To test emitter with exit condition"""
    name = models.CharField(u'Titre', max_length=255)
    emitter = True

    @staticmethod
    def get_xbus_event_type(event_type):
        """Get the event type"""
        return 'try_{event_type}'.format(event_type=event_type)

    def get_xbus_fields(self):
        fields = {'name': self.name}
        return fields

    def get_admin_url(self):
        """Get the admin url"""
        return ''

    def condition_to_exit(self):
        return True


class Consumer(XbusAwareMixin, models.Model):
    """To test consumer"""
    name = models.CharField(u'Titre', max_length=255)
