from datetime import datetime, timedelta
import logging

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from xbus.models import Event

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete xbus event from db older than a specific period or date"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'period',
            nargs='?', type=int, default=0,
            help="Set a number of days")

        # Named (optional) arguments
        parser.add_argument(
            '--date',
            nargs='?', dest='date', type=str, default='',
            help='Use a date in the format yyyy-mm-dd rather than a period')
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    def handle(self, *args, **options):
        date = options['date']
        days = options['period']
        interactive = options['interactive']

        if days:
            ctime = datetime.now() - timedelta(days)
        else:
            ctime = date
        try:
            query = Event.objects.filter(ctime__lte=ctime)
            nb = query.count()
        except ValidationError:
            raise CommandError(
                'Wrong argument format, read --help for more help')
        else:
            logger.info(
                'The {nb} xbus events older than {ctime} will be delete'
                .format(nb, ctime))
            if interactive:
                answer = raw_input('Are you sure ? (yes or no): ')
            else:
                answer = 'yes'
            if answer.lower() in ['yes', 'y']:
                query.delete()
                print "Deleted"
            else:
                print "Aborted"
