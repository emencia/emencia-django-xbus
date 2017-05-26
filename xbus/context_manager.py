from contextlib2 import contextmanager

from django.db.models import signals

from xbus.models import send_to_xbus


@contextmanager
def disconnect_xbus_send():
    """To deactivate the signal that is sent to xbus"""
    signals.post_save.disconnect(send_to_xbus, dispatch_uid='send_to_xbus')
    yield
    signals.post_save.connect(send_to_xbus, dispatch_uid='send_to_xbus')
