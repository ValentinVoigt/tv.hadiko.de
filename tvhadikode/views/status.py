# -*- encoding: utf-8 -*-

import json
import urllib.request

from pyramid.view import view_config

from tvhadikode.scripts.import_services import extract_urls
from tvhadikode.views.base import BaseView
from tvhadikode.models import DBSession, Service

def iterate_urls(request, path):
    urls = extract_urls(request.registry.settings)
    for url in urls:
        data = urllib.request.urlopen("%s%s" % (url, path)).read()
        data = json.loads(str(data, "utf-8"))
        yield data

class StatusViews(BaseView):

    @view_config(route_name='status', renderer='tvhadikode:templates/status.mak')
    def status(self):
        return {}

    @view_config(route_name='ajax.status.traffic', renderer='tvhadikode:templates/ajax/status_traffic.mak')
    def status_traffic(self):
        traffic = []
        for data in iterate_urls(self.request, "/monitor/channels_traffic.json"):
            for i in data:
                if i['name'] != "" and i['traffic'] != 0:
                    traffic.append(i)
        traffic.sort(key=lambda i: i['name'])

        services = DBSession.query(Service).all()
        services = dict([(service.name, service) for service in services])

        return {'traffics': traffic, 'services': services}

    @view_config(route_name='ajax.status.signal_clients', renderer='tvhadikode:templates/ajax/status_signal_clients.mak')
    def status_signal(self):
        status = []
        for data in iterate_urls(self.request, "/monitor/state.json"):
            status.append(data)

        services = DBSession.query(Service).all()
        services = dict([(service.name, service) for service in services])

        return {'status': status, 'services': services}
