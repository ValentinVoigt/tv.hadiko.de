# -*- encoding: utf-8 -*-

from pyramid.view import view_config

from tvhadikode.utils.dbhelpers import get_by_or_404
from tvhadikode.models import Service
from tvhadikode.views.base import BaseView

class ServiceViews(BaseView):

    @view_config(route_name='service', renderer='tvhadikode:templates/service.mak')
    def overview(self):
        service = get_by_or_404(Service, slug=self.request.matchdict.get('service'))
        return {'service': service}
