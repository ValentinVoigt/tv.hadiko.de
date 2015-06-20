# -*- encoding: utf-8 -*-

from pyramid.view import view_config

from tvhadikode.models import DBSession, Service

@view_config(route_name='home', renderer='tvhadikode:templates/epg.mak')
def my_view(request):
    services = DBSession.query(Service).order_by('name').all()
    return {'services': services, 'project': 'tv.hadiko.de'}
