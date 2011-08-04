from dexf.json import JSONEncoder, JSONDecoder
from django.conf import settings
from django.core import validators
from django.forms import CharField, FileField
from django.forms.util import flatatt
from django.utils.encoding import force_unicode, smart_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from dexf import json


class CsvFileField(FileField):
    def clean(self, value):
        value = super(FileField, self).clean(value)
        try:
            return  re.compile(value)
        except:
            raise ValidationError(_("'%s' is not a valid regex pattern" % value))
        #return value

class RegularExpressionField(CharField):
    def clean(self, value):
        value = super(RegularExpressionField, self).clean(value)
        try:
            return  re.compile(value)
        except:
            raise ValidationError(_("'%s' is not a valid regex pattern" % value))

class ClassPathField(CharField):
    """
    >>> c = ClassPathField()
    >>> c.clean("aa.bb")
    
    """
    def __init__(self, *args, **kwargs):
        super(ClassPathField, self).__init__(*args, **kwargs)

    def clean(self, value):
        try:
            path, classname = value.split(".", -1)
            path.split(".")
            assert re.match("^[a-zA-Z]*$", classname)
        except:
            raise ValidationError(_("'%s' is not a valid classname" % value))
        return value

class DictField(CharField):

    def __init__(self, encoding=settings.DEFAULT_CHARSET, max_length=None, min_length=None, *args, **kwargs):
        self.encoding = encoding
        super(DictField, self).__init__(max_length, min_length, *args, **kwargs)


    def prepare_value(self, value):
        # value is a dict we want to edit the dicte via TextInput widgtet
        return JSONEncoder(self.encoding).encode(value)

    def to_python(self, value):
        return JSONDecoder(self.encoding).decode(value)
#        return value

