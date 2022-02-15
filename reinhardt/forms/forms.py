from django import forms
from django.conf import settings
from django.forms import NullBooleanSelect

from .mixins import SearchFormMixin

DEFAULT_DATEFIELD_FORMAT = '%m/%d/%Y'
DEFAULT_TIMEFIELD_FORMAT = '%I:%M %p'
DEFAULT_DATETIMEFIELD_FORMAT = '%m/%d/%Y %I:%M %p'


def datetime_formfield_callback(f, **kwargs):
    """
    Overrides Django formfield widget default values
    """
    formfield = f.formfield(**kwargs)

    if isinstance(formfield, forms.DateField):
        try:
            formfield.widget.format = settings.DEFAULT_DATEFIELD_FORMAT
        except AttributeError:
            formfield.widget.format = DEFAULT_DATEFIELD_FORMAT

    if isinstance(formfield, forms.TimeField):
        try:  # set default
            formfield.input_formats = [settings.DEFAULT_TIMEFIELD_FORMAT]
        except AttributeError:
            formfield.input_formats = [DEFAULT_TIMEFIELD_FORMAT]

    if isinstance(formfield, forms.DateTimeField):
        try:  # set default
            formfield.input_formats = [settings.DEFAULT_DATETIMEFIELD_FORMAT]
        except AttributeError:
            formfield.input_formats = [DEFAULT_DATETIMEFIELD_FORMAT]

    return formfield


class ModelFormMetaclass(forms.models.ModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        if 'formfield_callback' not in attrs or not attrs['formfield_callback']:
            attrs['formfield_callback'] = datetime_formfield_callback
        return super(ModelFormMetaclass, mcs).__new__(mcs, name, bases, attrs)


class ModelForm(forms.ModelForm):
    REQUIRED_FIELD_ERROR = 'This field is required'
    __metaclass__ = ModelFormMetaclass

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        required_fields = self.Meta.required_fields if hasattr(self.Meta, 'required_fields') else tuple()
        for field in required_fields:
            self.fields[field].required = True

        hidden_fields = self.Meta.hidden_fields if hasattr(self.Meta, 'hidden_fields') else tuple()
        for field in hidden_fields:
            self.fields[field].widget = forms.HiddenInput()


class SearchFormDX(SearchFormMixin, forms.Form):
    pass


class ModelSearchFormDX(SearchFormMixin, ModelForm):
    """
    Django Model form with SearchFormMixin to create an Advanced Search
    form using multiple fields and filters

    Allows filtering a queryset using a list of fields, Q objects and custom
    filter methods

    """
    required_fields = []
    extra_kwargs = {}

    def clean(self):
        # disables unique check
        # https://github.com/django/django/blob/master/django/forms/models.py#L287
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        """
        Disables the require property of all form fields, allowing them to be
        used as optional search fields.
        """
        if 'extra_kwargs' in kwargs:
            self.extra_kwargs = kwargs.pop('extra_kwargs')
        super(ModelSearchFormDX, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in self.required_fields:
                self.fields[field].required = False


class SimpleSearchForm(ModelSearchFormDX):
    """
    Model Search Form with a single search field, provides similar
    functionality to django-admin search box

    Allows filtering a queryset using a list of fields, Q objects and custom
    filter methods

    :fields:
            - search

    """
    search = forms.CharField(max_length=200, required=False)
    search_placeholder = ''

    class Meta:
        fields = ('search',)

    def __init__(self, *args, **kwargs):
        """
        Disables the require property of all form fields, allowing them to be
        used as optional search fields.
        """
        super(SimpleSearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget = forms.TextInput(
            attrs={'placeholder': self.search_placeholder}
        )


class CustomNullBooleanSelect(NullBooleanSelect):
    """
    An overriden Select widget to be used with NullBooleanField.
    Takes a kwarg "null_label" that indicates the text on the null option.
    """
    def __init__(self, attrs=None, null_label=None, true_label=None, false_label=None):
        if null_label is None:
            null_label = 'Unknown'
        if true_label is None:
            true_label = 'True'
        if false_label is None:
            false_label = 'False'
        choices = (
            ('1', null_label),
            ('2', true_label),
            ('3', false_label)
        )
        super(NullBooleanSelect, self).__init__(attrs, choices)


class ReportSelector(forms.Form):
    """
    Form used for report views to provide a dropdown of available reports
    """
    get_reports = forms.ChoiceField(choices=[('', 'Select Report')])

    def __init__(self, user, reports_list, *args, **kwargs):
        super(ReportSelector, self).__init__(*args, **kwargs)
        self.fields['get_reports'].choices += [
            (k, v['name']) for k, v in reports_list.items()
        ]
