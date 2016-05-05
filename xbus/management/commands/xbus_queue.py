# Import from the Standard Library
import logging
from optparse import make_option
from os import fdopen
import sys
from time import sleep
from traceback import format_exc

# Import from Django
from django.core.management.base import NoArgsCommand

# Other
import msgpack

# Import from here
from xbus.models import Event
from xbus import api


admin_logger = logging.getLogger("django.request")

class Command(NoArgsCommand):

    option_list = NoArgsCommand.option_list + (
        make_option(
            '--daemon', action='store_true', default=False,
            help="Daemonize"
        ),
        make_option(
            '--in', type='int',
            help='limit number of incoming events to handle'
        ),
        make_option(
            '--out', type='int',
            help='limit number of outcoming events to handle',
        ),
        make_option(
            '--disable_out', action='store_true', default=False,
            help='Disable outgoing messages',
        ),
        make_option(
            '--disable_in', action='store_true', default=False,
            help='Disable incoming messages',
        ),
    )

    def queue_run_in(self, limit=None):
        pending = Event.objects.filter(state='pending', direction='in')
        pending = pending.order_by('pk')
        if limit is not None:
            pending = pending[:limit]

        for event in pending:
            event_type = event.event_type
            handler = api.registry.get(event_type)

            if handler is None:
                event.state = 'error'
                event.comment = 'unexpected event type "%s"' % event_type
                event.save()
                continue

            try:
                item = msgpack.unpackb(event.item, encoding='utf-8')
                obj = handler(event.xref, item)
            except Exception:
                event.state = 'error'
                event.comment = format_exc()
                event.save()
                admin_logger.error("XBUS - Connection error - IN %s", event.comment)
            else:
                event.state = 'done'
                event.comment = u''  # Override previous error, may happen
                if obj is not None:
                    if hasattr(obj, 'get_admin_url'):
                        event.admin_url = obj.get_admin_url()
                event.save()

    def queue_run_out(self, limit=None):
        """
        Sends (at most 100) pending events to xbus. Returns the number
        of pending events over 100.
        """
        pending = Event.objects.filter(state='pending', direction='out')
        pending = pending.order_by('pk')
        if limit is not None:
            pending = pending[:limit]

        # Avoid login if there is nothing to send
        left = 0
        n = pending.count()
        if n == 0:
            return left

        if n > 100:
            pending = pending[:100]
            left = n - 100

        conn, token = api.new_connection_to_xbus()

        for event in pending:
            try:
                ret, event_id = api._xbus_send_event(conn, token, event)
            except Exception:
                event.state = 'error'
                event.comment = format_exc()
                event.save()
                admin_logger.error("XBUS - Connection error - OUT %s", event.comment)
            else:
                event.state = 'done'
                event.event_id = event_id
                event.comment = u''  # Override previous error, may happen
                event.save()

            sleep(0.1) # Wait for Xbus to digest

        conn.logout(token)
        conn.close()
        return left

    def handle_noargs(self, **kw):
        if kw["daemon"]:
            sys.stdout = fdopen(sys.stdout.fileno(), 'w', 0)
            while True:
                if not kw["disable_in"]:
                    self.queue_run_in(kw['in'])

                if not kw["disable_out"]:
                    left = self.queue_run_out(kw['out'])
                else:
                    left = 0

                if left == 0:
                    sleep(5)
        else:
            if not kw["disable_in"]:
                self.queue_run_in(kw['in'])

            if not kw["disable_out"]:
                self.queue_run_out(kw['out'])
