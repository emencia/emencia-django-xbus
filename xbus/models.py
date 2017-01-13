import logging

# Import from Django
from django.db import models
from django.db.models import Model, Manager
from django.db.models import (
    BinaryField, CharField, DateTimeField, TextField, NullBooleanField,
)
from django.utils.translation import ugettext as _

# Other
from django_extensions.db.fields import UUIDField

from xbus.api import send_event
from xbus.constants import XREF_LENGTH, DIRECTION_CHOICES, STATE_CHOICES


logger = logging.getLogger(__name__)


class XbusManager(Manager):
    def get_by_natural_key(self, xref, odoo_created):
        return self.get(xref=xref)


class XbusAwareMixin(Model):
    """
    Base class for models to be synchronised through Xbus.

    The odoo_created field represents the fact that we already sent a
    create xbus-event for this object. This will be used because Django
    creation step happens when the object is mostly empty, which is not
    an interesting state for Odoo. We might want to wait for certain fields
    to be filled to send a create xbus-event.
    """
    # TODO
    # 1. Add data migrations to set xref for existing objects
    # 2. Then set unique=True
    xref = UUIDField(_(u'External Ref'), null=True, blank=True,
                     max_length=XREF_LENGTH)
    odoo_created = NullBooleanField(default=False, editable=False)
    emitter = False
    auto_save = True
    objects = XbusManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return (self.xref, self.odoo_created)

    def get_xbus_fields(self):
        raise NotImplementedError()

    @staticmethod
    def get_xbus_event_type(event_type):
        """Returns the event_type which will be used to contact xbus

        @param event_type: The type created or updated
        @type  param: str

        @return:  The event type
        @rtype :  str
        """
        raise NotImplementedError()

    def get_admin_url(self):
        """Get the admin url"""
        raise NotImplementedError()

    def odoo_creation_condition(self):
        """
            Returns the True if the condition for creation on the odoo side
            is met.
        """
        return True

    def save(self, *args, **kwargs):
        """To send data to xbus"""
        if self.emitter and self.auto_save:
            xbus_fields = self.get_xbus_fields()
            admin_url = self.get_admin_url()

            if not self.pk:
                event_type = self.get_xbus_event_type('created')
                logger.info(
                    u'A new item is created and synchronize {xref}'.format(
                        xref=self.xref))
            else:
                event_type = self.get_xbus_event_type('updated')
                logger.info(
                    u'A new item is updated and synchronize {xref}'.format(
                        xref=self.xref))
            send_event(self, event_type, xbus_fields, admin_url=admin_url)

        super(XbusAwareMixin, self).save(*args, **kwargs)


class Envelope(models.Model):
    """To store envelope"""
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    envelope_id = models.CharField(max_length=80, null=True, blank=True)
    direction = models.CharField(max_length=25, choices=DIRECTION_CHOICES)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)


class Event(Model):
    ctime = DateTimeField(auto_now_add=True, null=True)

    # Identify the object in the database and its version
    xref = CharField(_(u'External Ref'), max_length=XREF_LENGTH)
    xbus_message_correlation_id = CharField(
        _(u'Message correlation id'), max_length=36)

    # Event type
    event_type = CharField(_(u'Event type'), max_length=80)
    event_id = CharField(_(u'Event id'), max_length=80, null=True, blank=True)

    comment = TextField(_(u'Comment'), blank=True)

    # Binary in msgpack format
    item = BinaryField(_(u'Event item'))
    admin_url = CharField(
        max_length=250, default="", editable=False, null=True)
    envelope = models.ForeignKey(Envelope, null=True)


class XbusSyncError(Exception):
    pass
