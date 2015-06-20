# -*- encoding: utf-8 -*-

from pyramid.view import view_config

from tvhadikode.models import DBSession, Service

from tvhadikode.views.base import BaseView

class HomeViews(BaseView):

    @view_config(route_name='home', renderer='tvhadikode:templates/epg.mak')
    def epg(self):
        services = DBSession.query(Service).order_by('name').all()
        return {'services': services}
