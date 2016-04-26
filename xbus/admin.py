# Import from the Standard Library
from pprint import pformat

# Import from Django
from django.contrib import admin

# Import msgpack
import msgpack

# Import from here
from .models import Event



def change_to_pending(modeladmin, request, queryset):
    for obj in queryset.iterator():
        obj.state = 'pending'
        obj.save()

change_to_pending.short_description = u'Change state to pending'


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'xref',
        'event_type', 'event_id',
        'direction', 'state',
        'ctime', 'id',
    )

    list_filter = ('direction', 'state', 'event_type')
    search_fields = ('xref', 'xbus_message_correlation_id', 'event_id')

    readonly_fields = ['to_admin_url', 'payload', 'ctime']

    actions = [change_to_pending]

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
