from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import _get_queryset 
from meteora import Meteora

def json( convert ):
    return HttpResponse(simplejson.dumps(convert), mimetype="text/plain")

def get_object_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs), True
    except queryset.model.DoesNotExist:
        m = Meteora(False,"No %s not matches the given query." % queryset.model._meta.object_name)
        return m.json_response(), False
