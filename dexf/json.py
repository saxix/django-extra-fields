from django.core.exceptions import ValidationError
from django.utils import simplejson as json
from django.conf import settings
from datetime import datetime
import time



class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        return json.JSONEncoder.default(self, obj)

    def encode(self, o):
        if not isinstance(o, dict):
            raise ValidationError('not a dict')
        return super(JSONEncoder, self).encode(o)


class JSONDecoder(json.JSONDecoder):
    def decode(self, json_string):
        json_data = json.loads(json_string)
        if json_data is None:
            return {}
        for key in json_data.keys():
            try:
                json_data[key] = datetime.fromtimestamp(time.mktime(time.strptime(json_data[key], "%Y-%m-%d %H:%M:%S")))
            except TypeError:
                # It's not a datetime/time object
                pass
        return json_data

  