# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext as _

XREF_LENGTH = 80
DIRECTION_CHOICES = (
    ('in', _(u'Incoming')),
    ('out', _(u'Outgoing')),
    ('immediate-out', _(u'Immediate-Out')),
)
STATE_CHOICES = (
    ('draft', _(u'Draft')),
    ('pending', _(u'Pending')),
    ('done', u'Done'),
    ('error', _(u'Error')),
)
CONSUMER_LISTEN = getattr(
    settings, 'XBUS_CONSUMER_LISTEN', u'tcp://127.0.0.1:4892')
CONSUMER_URL = getattr(settings, 'XBUS_CONSUMER_URL', u'tcp://127.0.0.1:4891')
CONSUMER_LOGIN = getattr(settings, 'XBUS_CONSUMER_LOGIN', u'consumer_role')
CONSUMER_PASSWORD = getattr(settings, 'XBUS_CONSUMER_PASSWORD', u'password')
