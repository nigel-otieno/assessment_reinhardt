import re
import unicodedata

from django.db.models.fields.related import RelatedField
from django.utils import six
from django.utils.encoding import force_text
from django.utils.functional import keep_lazy
from django.utils.safestring import mark_safe, SafeText


def snakify(value):
    """
    Converts to ASCII. Converts spaces to underscores. Removes characters that
    aren't alphanumerics, underscores, or hyphens. Converts to lowercase.
    Also strips leading and trailing whitespace.

    :param string value: unsanitized value

    :returns: snakified value

    Usage:
        .. code-block:: python
            :linenos:

            >>> snakify('polls-report May 1, 2016')
            u'polls_report_may_1_2016'

    """
    value = force_text(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return mark_safe(re.sub('[-\s]+', '_', value))


snakify = keep_lazy(snakify, six.text_type, SafeText)


def get_child(obj):
    """
        Returns the utilized child class instance of a superclass instance.

        :param Model obj: Django Model instance

        :returns: Subclass instance or None
    """
    try:
        subclass_instance_name = next(
            rel_obj.name for rel_obj in obj._meta.get_all_related_objects()
            if rel_obj.parent_link and hasattr(obj, rel_obj.name)
        )
    except StopIteration:
        return None
    return getattr(obj, subclass_instance_name)


def _hasfield(model_fields, field_name):
    """
    Check if field name exists in list of model fields

    :param list model_fields: List of Django Model object fields
    :param string field_name: attribute string, dotted or dunderscored.
    example: 'user.first_name' or 'user__first_name'

    :returns: Field object or False

    """
    for field in model_fields:
        if field.name == field_name:
            return field
    return False


def hasfield(model, field_name):
    """
    Returns whether the specified field_name string is a valid field on
     model or its related models

    :param Model model: Django Model object
    :param string field_name: attribute string, dotted or dunderscored.
     example: 'user.first_name' or 'user__first_name'

    :returns: Field object or False

    Usage:
        .. code-block:: python
            :linenos:

            >>> hasfield(Poll, 'question')
            Django Model
            >>> hasfield(Poll, 'user__name')
            Django Model
            >>> hasfield(Poll, 'user.username')
            Django Model
            >>> hasfield(Poll, 'user.full_name')
            False # full_name is a property method not a field
    """

    field_names = field_name.replace('__', '.').split('.')
    model_fields = model._meta.fields

    for idx, field_name in enumerate(field_names):
        related_field = _hasfield(model_fields, field_name)

        if not related_field or (related_field and idx == len(field_names) - 1):
            return related_field

        # If field is a ForeignKey, ManyToManyField, or OneToOneField, look through related model
        if isinstance(related_field, RelatedField):
            model_fields = related_field.related_model._meta.fields

    return False


def replace_key(old_key, new_key, dictionary):
    if old_key in dictionary:
        value = dictionary.pop(old_key)
        dictionary[new_key] = value
    return dictionary