# Imports from django
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Import from this project
from project.xbus import api


def update_object(obj, **kw):
    """
    Helper function to update an object with the given new values.
    """
    for key, value in kw.items():
        setattr(obj, key, value)

    obj.save()


def kwargs_from_dict(item, keys, map_fields={}):
    """
    Helper function that takes an item as sent by Xbus, and returns a dict that
    can be used to create or update an object.
    """
    kw = {}
    for key in keys:
        if key in item:
            kw[map_fields.get(key, key)] = item[key]

    return kw


def kwargs_from_instance(instance, fields, map_fields):
    """
    Read from an object the fields we need to export.
    - instance: object
    - fields: list with the fields that expect odoo
    - map_fields: some fields don't have the same name, with this dict we
                  convert the field names {'odoo_field': 'django_field'}
                  If the name is the same is not necessary to add the
                  conversion
    """
    kw = {}
    for field in fields:
        key = map_fields.get(field, field)
        kw[field] = getattr(instance, key)

    return kw


def has_updated_fields(updated_fields, fields, map_fields={}):
    """
    Check if some the fields we track the info are in the list of updated
    fields
    """

    # If the list of update fields are empty we can't known the exact update
    # fields, then we consider that the fields we track has been updated
    if not updated_fields:
        return True

    for field in fields:
        key = map_fields.get(field, field)
        if key in updated_fields:
            return True

    return False


def get_handler(event_type):
    return api.registry.get(event_type)


def process_incoming_data(event_type, xbus_dict):
    xref = xbus_dict['xref']
    handler = get_handler(event_type)
    if handler is None:
        raise Exception("unknown event_type: %s" % event_type)

    return handler(xref, xbus_dict)


def get_object(model, **kw):
    """
    Helper function that returns the object asked for, or None if it is not
    found.
    """
    try:
        return model.objects.get(**kw)
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned:
        absolute_module_path = '.'.join((model.__module__, model.__name__))
        kw_list = ', '.join(['%s=%s' % (key, val) for key, val in kw.items()])
        message = (
            "The following query : %s.get(%s), should have returned only "
            "one result, but instead returned multiple objects:\n"
        ) % (absolute_module_path, kw_list)

        total = 0
        for obj in model.objects.filter(**kw):
            if total > 8:
                message += "- ..."
                break

            if hasattr(obj, 'get_admin_url'):
                url = obj.get_admin_url()
            message += "- %s\n" % url
            total += 1

        raise MultipleObjectsReturned(message)
