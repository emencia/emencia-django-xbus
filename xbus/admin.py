# Import from the Standard Library
from pprint import pformat

# Import from Django
from django.contrib import admin

# Import msgpack
import msgpack

# Import from here
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'xref', 'xbus_message_correlation_id',
        'event_type', 'direction', 'state',
        'ctime', 'id',
    )

    list_filter = ('direction', 'state', 'event_type')
    search_fields = ('xref', 'xbus_message_correlation_id')

    readonly_fields = ['to_admin_url', 'payload', ]

    def payload(self, obj):
        item = msgpack.unpackb(obj.item, encoding='utf-8')
        item = pformat(item)
        return '<pre>%s</pre>' % item
    payload.allow_tags = True

    def to_admin_url(self, obj):
        url = '<a href="{url}">{url}</a>'.format(url=obj.admin_url)
        return url if obj.admin_url else 'Unspecified'
    to_admin_url.allow_tags = True


admin.site.register(Event, EventAdmin)
