# Imports from libs
from IPython.terminal.embed import InteractiveShellEmbed
import msgpack

# Imports from django
from django.core.management.base import LabelCommand
from django.core.exceptions import ObjectDoesNotExist

# Imports from xbus
from xbus.utils import process_incoming_data, get_handler
from xbus.api import send_event
from xbus.models import Event


banner = (
    "Hi there. This is an interactive IPython shell."
    "Type help_xbus_commands() for the help.\n"
    "Xbus default event_type is: %s.\n"
    "Commands: create_event(xbus_dict), run_callback(xbus_dict), "
    "get_object(model, **kwargs), replay_event(event_pk)"
)

COMMAND_HELP_MSG = (
    "Apart from django stuff usually available in django-instance shell, you\n"
    "can call:\n"
    "\n"
    "- create_event(xbus_dict, [event_type]): creates an Xbus Event that\n"
    "will eventually be processed by xbus_queue, provided it is running.\n"
    "\n"
    "- run_callback(xbus_dict, [event_type]): directly calls the registered\n"
    "callback for the event_type.\n"
    "\n"
    "- replay_event(event_pk): Call an previously stored event\n"
    "In both functions, the default event_type will be the one provided to\n"
    "this command (i.e. now: %s), \n"
    "and in both functions, you'll have to provide the xbus dict.\n"
)


ipshell = InteractiveShellEmbed(
    exit_msg='Leaving Interpreter, back to program.'
)


class FakeXbusAwareObject():
    # Temporary, until we can remove need for 'instance' in send_event
    # signature.
    xref = ''


class Command(LabelCommand):
    def replay_event(self, obj_id):
        try:
            event = Event.objects.get(pk=obj_id)
        except ObjectDoesNotExist:
            return None

        xbus_dict = msgpack.unpackb(event.item, encoding='utf-8')
        if event.direction == 'in':
            return self.run_callback(xbus_dict, event.event_type)
        elif event.direction == 'out':
            # Let's keep the thing simple
            # return self.create_event(xbus_dict, event.event_type)
            return None
        else:
            return None

    def create_event(self, xbus_dict, event_type=None):
        if event_type is None:
            event_type = self.event_type
        instance = FakeXbusAwareObject()
        instance.xref = xbus_dict['xref']
        return send_event(instance, event_type, xbus_dict)

    def run_callback(self, xbus_dict, event_type=None):
        if event_type is None:
            event_type = self.event_type
        return process_incoming_data(event_type, xbus_dict)

    def command_help(self):
        print COMMAND_HELP_MSG % self.event_type

    def handle_label(self, label, **kw):
        self.event_type = label

        handler = get_handler(self.event_type)
        if handler is None:
            print "!warning!: unregistered event type: %s" % self.event_type

        self.command_help
        self.create_event
        self.run_callback
        self.replay_event

        ipshell.banner1 = banner % label
        ipshell()
