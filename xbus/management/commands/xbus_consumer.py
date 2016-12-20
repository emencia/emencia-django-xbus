"""
Requirements besides Django:

$ pip install msgpack-python
$ hg clone https://bitbucket.org/xcg/zmq_rpc
$ pip install zmq_rpc/pyzmq/
"""

# Import from the Standard Library
from datetime import datetime
from threading import Thread
from time import sleep
import logging

# Import from Django
from django.conf import settings
from django.core.management.base import NoArgsCommand

# Import from msgpack
import msgpack

# Import from zmq_rpc
from zmq_rpc.server import ZmqRpcServer, RpcMethod
from zmq_rpc.client import ZmqRpcClient

# Import from xbus
from xbus.models import Event
from xbus.api import _send_healtcheck_event

logger = logging.getLogger(__name__)


class Consumer(ZmqRpcServer):

    def __init__(self, *args, **kw):
        super(Consumer, self).__init__(*args, **kw)
        self.event_id_to_type = {}

    @RpcMethod
    def get_metadata(self):
        now = unicode(datetime.now().isoformat())
        return {
            u'name': settings.XBUS_CONSUMER_NAME,
            u'version': 0.1,
            u'api_version': 0.1,
            u'host': u'localhost',
            u'start_date': now,
            u'local_time': now,
        }

    @RpcMethod
    def ping(self, token):
        return token

    @RpcMethod
    def has_clearing(self):
        return False, None # data clearing not supported

    @RpcMethod
    def has_immediate_reply(self):
        return False, [] # immediate replies not supported

    #
    # API to read data
    #
    @RpcMethod
    def start_event(self, envelope_id, event_id, type_name):
        logger.debug(u'Start event')
        self.event_id_to_type[event_id] = type_name
        return True, [] # Ok

    @RpcMethod
    def send_item(self, envelope_id, event_id, indices, data):
        item = data
        event_type = self.event_id_to_type[event_id]
        healthcheck = getattr(
            settings, 'XBUS_CONSUMER_HEALTCHECK', 'healthcheck_consumer')

        if event_type == healthcheck:
            logger.info(u'Received the healtcheck message')
            return _send_healtcheck_event(data)

        data = msgpack.unpackb(data, encoding='utf-8', use_list=False)

        xbus_message_correlation_id = data['xbus_message_correlation_id']
        xref = data['xref']
        Event.objects.create(
            direction='in',
            state='pending',
            xbus_message_correlation_id=xbus_message_correlation_id,
            xref=xref,
            event_type=event_type,
            item=item,
        )

        return True, [] # Ok

    @RpcMethod
    def end_event(self, envelope_id, event_id):
        del self.event_id_to_type[event_id]
        return True, []

    @RpcMethod
    def end_envelope(self, envelope_id):
        return True, []


# URL the consumer will listen to
CONSUMER_LISTEN = getattr(settings, 'XBUS_CONSUMER_LISTEN', u'tcp://127.0.0.1:4892')

# Connect to Xbus.broker
CONSUMER_URL = getattr(settings, 'XBUS_CONSUMER_URL', u'tcp://127.0.0.1:4891')
CONSUMER_LOGIN = getattr(settings, 'XBUS_CONSUMER_LOGIN', u'consumer_role')
CONSUMER_PASSWORD = getattr(settings, 'XBUS_CONSUMER_PASSWORD', u'password')


class Command(NoArgsCommand):

    def register_to_xbus(self):
        # Wait 1s to give the server time to start
        # (because XBus will contact the server)
        sleep(1)

        # Connect to XBus
        client = ZmqRpcClient(CONSUMER_URL, timeout=1000)
        token = client.login(CONSUMER_LOGIN, CONSUMER_PASSWORD)
        if not token:
            logger.error(u'Authentication failed')
            return

        client.register_node(token, CONSUMER_LISTEN)
        logger.info(u'Registration done')

    def handle_noargs(self, **kw):
        thread = Thread(target=self.register_to_xbus)
        thread.start()

        # Run server
        server = Consumer(CONSUMER_LISTEN)
        logger.info(u'Server run listening {consumer_listen}'.format(
            consumer_listen=CONSUMER_LISTEN))
        server.run()
