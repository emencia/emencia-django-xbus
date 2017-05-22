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
        """docstring for get_xbus_event_type"""
        return 'try_{event_type}'.format(event_type=event_type)

    def get_xbus_fields(self):
        fields = {'name': self.name}
        return fields

    def get_admin_url(self):
        """docstring for get_admin_url"""
        return ''


class Consumer(XbusAwareMixin, models.Model):
    """To test consumer"""
    name = models.CharField(u'Titre', max_length=255)
