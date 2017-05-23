import logging

# Import from Django
from django.db import models
from django.db.models import Model, Manager
from django.db.models import (
    BinaryField, CharField, DateTimeField, TextField, NullBooleanField,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    def condition_to_exit(self):
        """Add a specific condition to exit

        @return:  The result of condition
        @rtype :  bool
        """
        return False


class Envelope(models.Model):
    """To store envelope"""
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    envelope_id = models.CharField(max_length=80, null=True, blank=True)
    direction = models.CharField(max_length=25, choices=DIRECTION_CHOICES)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)

    def __unicode__(self):
        return self.pk


class Event(Model):
    ctime = DateTimeField(auto_now_add=True, null=True)

    # Identify the object in the database and its version
    xref = CharField(_(u'External Ref'), max_length=XREF_LENGTH)
    xbus_message_correlation_id = CharField(
        _(u'Message correlation id'), max_length=36)

    # Event type
    event_type = CharField(_(u'Event type'), max_length=80)
    event_id = CharField(_(u'Event id'), max_length=80, null=True, blank=True)
    direction = models.CharField(
        max_length=25, choices=DIRECTION_CHOICES, null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, null=True)
    comment = TextField(_(u'Comment'), blank=True)

    # Binary in msgpack format
    item = BinaryField(_(u'Event item'))
    admin_url = CharField(
        max_length=250, default="", editable=False, null=True)
    envelope = models.ForeignKey(Envelope, null=True)


class XbusSyncError(Exception):
    pass


@receiver(post_save, dispatch_uid='send_to_xbus')
def send_to_xbus(sender, instance, created, **kwargs):
    if issubclass(sender, XbusAwareMixin):
        if instance.emitter:
            if instance.condition_to_exit():
                return

            xbus_fields = instance.get_xbus_fields()
            admin_url = instance.get_admin_url()

            if created:
                event_type = instance.get_xbus_event_type('created')
                logger.info(
                    u'A new item is created and synchronize {xref}'.format(
                        xref=instance.xref))
            else:
                event_type = instance.get_xbus_event_type('updated')
                logger.info(
                    u'A new item is updated and synchronize {xref}'.format(
                        xref=instance.xref))
            send_event(instance, event_type, xbus_fields, admin_url=admin_url)
