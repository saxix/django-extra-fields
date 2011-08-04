import django
from dexf.json import JSONEncoder, JSONDecoder
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.utils.text import capfirst
import re
import dexf.forms
import datetime
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils import simplejson as json


class ClassPathField(models.TextField):
    def __init__(self, verbose_name=None, name=None, present_in_path=False, **kwargs):
        self.present_in_path = present_in_path
        models.Field.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': dexf.forms.ClassPathField}
        defaults.update(kwargs)
        return models.Field.formfield(self, **defaults)

class RegularExpressionField(models.CharField):

    def to_python(self, value):
        if value is None:
            return value
        elif isinstance(value, basestring):
            return re.compile(value)

    def formfield(self, **kwargs):
        defaults = {'widget': dexf.forms.RegularExpressionField}
        defaults.update(kwargs)
        return models.Field.formfield(self, **defaults)

class StringDict(dict):
    """
    >>> d = StringDict()
    >>> d['22'] = 'aa'
    >>> d[22] == d['22']
    True
    >>> d[22] = 'bb'
    >>> d[22] == d['22'] == 'bb'
    True
    """
    def __setitem__(self, i, y):
        return super(StringDict, self).__setitem__(str(i), y)

    def __getitem__(self, y):
        return super(StringDict, self).__getitem__(str(y))


class DictField(models.TextField):

    def __init__(self, verbose_name=None, name=None, encoding=settings.DEFAULT_CHARSET, primary_key=False, max_length=None, unique=False, blank=False,
                 null=False, db_index=False, rel=None, default=NOT_PROVIDED, editable=True, serialize=True,
                 unique_for_date=None, unique_for_month=None, unique_for_year=None, choices=None, help_text='',
                 db_column=None, db_tablespace=None, auto_created=False, validators=[], error_messages=None):
        self.encoding = encoding
        super(DictField, self).__init__(verbose_name, name, primary_key, max_length, unique, blank, null, db_index, rel,
                                        default, editable, serialize, unique_for_date, unique_for_month, unique_for_year
                                        , choices, help_text, db_column, db_tablespace, auto_created, validators,
                                        error_messages)

    def _dumps(self, data):
        return JSONEncoder(self.encoding).encode(data)

    def _loads(self, str):
        return JSONDecoder(self.encoding).decode(str)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        return self._dumps(value)

    def contribute_to_class(self, cls, name):
        self.class_name = cls
        super(DictField, self).contribute_to_class(cls, name)
        models.signals.post_init.connect(self.post_init)

        def get_json(model_instance):
            return self._dumps(getattr(model_instance, self.attname, None))
        setattr(cls, 'get_%s_json' % self.name, get_json)

        def set_json(model_instance, json):
            return setattr(model_instance, self.attname, self._loads(json))
        setattr(cls, 'set_%s_json' % self.name, set_json)

    def post_init(self, **kwargs):
        if 'sender' in kwargs and 'instance' in kwargs:
            if kwargs['sender'] == self.class_name and hasattr(kwargs['instance'], self.attname):
                value = self.value_from_object(kwargs['instance'])
                if (value):
                    setattr(kwargs['instance'], self.attname, StringDict(self._loads(value)))
                else:
                    setattr(kwargs['instance'], self.attname, None)


    def formfield(self, **kwargs):
        kwargs.update({'form_class': dexf.forms.JSONField, 'encoding':self.encoding})
#        kwargs.update({'form_class': django.forms.CharField})
        return super(PreferencesField, self).formfield(**kwargs)
