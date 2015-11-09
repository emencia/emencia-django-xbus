# Import from the Standard Library
import logging
from optparse import make_option
from os import fdopen
import sys
from time import sleep
from traceback import format_exc

admin_logger = logging.getLogger("django.request")

# Import from Django
from django.core.management.base import NoArgsCommand

# Other
import msgpack

# Import from here
from project.xbus.models import Event
from project.xbus import api


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
        pending = Event.objects.filter(state='pending', direction='out')
        pending = pending.order_by('pk')
        if limit is not None:
            pending = pending[:limit]

        # Avoid login if there is nothing to send
        if pending.count() == 0:
            return

        conn, token = api.new_connection_to_xbus()

        for event in pending:
            try:
                api._xbus_send_event(conn, token, event)
            except Exception:
                event.state = 'error'
                event.comment = format_exc()
                event.save()
                admin_logger.error("XBUS - Connection error - OUT %s", event.comment)
            else:
                event.state = 'done'
                event.comment = u''  # Override previous error, may happen
                event.save()

        conn.logout(token)
        conn.close()

    def handle_noargs(self, **kw):
        if kw["daemon"]:
            sys.stdout = fdopen(sys.stdout.fileno(), 'w', 0)
            while True:
                self.queue_run_in(kw['in'])
                self.queue_run_out(kw['out'])
                sleep(5)
        else:
            self.queue_run_in(kw['in'])
            self.queue_run_out(kw['out'])
