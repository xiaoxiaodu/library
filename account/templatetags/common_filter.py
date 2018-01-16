# -*- coding:utf-8 -*-

import json
from django import template

register = template.Library()


@register.filter(name='to_json')
def to_json(obj):
    if not obj:
        return ""
    else:
        result = json.dumps(obj)
        return result
