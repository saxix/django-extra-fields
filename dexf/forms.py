from django.forms.fields import CharField, FileField
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CsvFileField(FileField):
    def clean(self, value):
        value = super(RegexField, self).clean(value)
        try:
            return  re.compile(value)
        except:
            raise ValidationError(_("'%s' is not a valid regex pattern" % value))
        #return value

class RegexField(CharField):
    def clean(self, value):
        value = super(RegexField, self).clean(value)
        try:
            return  re.compile(value)
        except:
            raise ValidationError(_("'%s' is not a valid regex pattern" % value))
