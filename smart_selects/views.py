from django.db.models import get_model
from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson
import locale
from smart_selects.utils import unicode_sorter


def filterchain(request, app, model, field, value, manager=None):
    Model = get_model(app, model)
    if value == '0':
        keywords = {str("%s__isnull" % field): True}
    else:
        keywords = {str(field): str(value)}
    if manager is not None and hasattr(Model, manager):
        queryset = getattr(Model, manager).all()
    else:
        queryset = Model.objects
    results = list(queryset.filter(**keywords))
    results.sort(cmp=locale.strcoll, key=lambda x: unicode_sorter(unicode(x)))
    result = []
    for item in results:
        result.append({'value': item.pk, 'display': unicode(item)})
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')


def filterchain_m2m(request, app, model, mapp, middle, field, value, manager=None):
    #middle = 'Standings'
    Model = get_model(app, model)
    Middle = get_model(mapp, middle)
    if manager is not None:
        raise HttpResponseServerError
    if value == '0':
        keywords = {str("%s__isnull" % field): True}
    else:
        keywords = {str(field): str(value)}
    if manager is not None and hasattr(Model, manager):
        queryset = getattr(Model, manager).all()
    else:
        queryset = Middle.objects
    results = list(queryset.filter(**keywords))
    results.sort(cmp=locale.strcoll, key=lambda x: unicode_sorter(unicode(x)))
    result = []
    for item in results:
        itemid = item.__dict__[model.lower() + '_id']
        result.append({'value': itemid, 'display': unicode(Model.objects.get(pk=itemid))})
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')


def filterchain_all(request, app, model, field, value):
    Model = get_model(app, model)
    if value == '0':
        keywords = {str("%s__isnull" % field): True}
    else:
        keywords = {str(field): str(value)}
    results = list(Model.objects.filter(**keywords))
    results.sort(cmp=locale.strcoll, key=lambda x: unicode_sorter(unicode(x)))
    final = []
    for item in results:
        final.append({'value': item.pk, 'display': unicode(item)})
    results = list(Model.objects.exclude(**keywords))
    results.sort(cmp=locale.strcoll, key=lambda x: unicode_sorter(unicode(x)))
    final.append({'value': "", 'display': "---------"})

    for item in results:
        final.append({'value': item.pk, 'display': unicode(item)})
    json = simplejson.dumps(final)
    return HttpResponse(json, mimetype='application/json')
