# Import from the Standard Library
from pprint import pformat

# Import from Django
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

# Import msgpack
import msgpack

# Import from here
from .models import Envelope, Event


def change_to_pending(modeladmin, request, queryset):
    for obj in queryset.iterator():
        obj.state = 'pending'
        obj.save()


change_to_pending.short_description = u'Change state to pending'


class EnvelopeAdmin(admin.ModelAdmin):
    """Admin of envelope"""
    list_display = (
        'envelope_id', 'created_at', 'show_event', 'direction', 'state')
    list_filter = ('state',)
    search_fields = ('envelope_id',)

    def show_event(self, obj):
        """To display event with a link"""
        all_event = ''

        for event in obj.event_set.all():
            url = reverse('admin:{app}_{model}_change'.format(
                app=event._meta.app_label, model=event._meta.model_name),
                args=(event.pk,))
            all_event += u'<a href="{url}">{pk} {event_id}</a><br />'.format(
                url=url, pk=event.pk, event_id=event.event_id)

        return format_html(all_event)


class EventAdmin(admin.ModelAdmin):
    list_display = ('xref', 'event_type', 'event_id', 'ctime', 'id')
    list_filter = ('event_type',)
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


admin.site.register(Envelope, EnvelopeAdmin)
admin.site.register(Event, EventAdmin)
