# -*- encoding: utf-8 -*-

from datetime import datetime

from pyramid.view import view_config

from sqlalchemy import and_
from sqlalchemy.orm import aliased, joinedload

from tvhadikode.models import DBSession, Service, Program
from tvhadikode.views.base import BaseView
from tvhadikode.utils.helpers import smartdate

class SearchViews(BaseView):

    @view_config(route_name='ajax.search.services', renderer='json')
    def search_services(self):
        now = datetime.now()
        current = aliased(Program)
        services = DBSession.query(Service, current)
        services = services.outerjoin(current, and_(current.sid==Service.sid, current.start<=now, current.end>=now))

        data = []
        for result in services.order_by(Service.name).all():
            service, current_program = result
            data.append({
                'service': service.name,
                'current_program': current_program.name if current_program else None,
                'url': self.request.route_path('service', service=service.slug)
            })
        return data

    @view_config(route_name='ajax.search.programs', renderer='json')
    def search_programs(self):
        now = datetime.now()
        query = self.request.matchdict.get('query')

        programs = DBSession.query(Program)
        programs = programs.options(joinedload('service'))
        programs = programs.filter(and_(Program.end>=now, Program.name.like('%' + query + '%')))

        data = []
        for program in programs.order_by(Program.start, Program.name).all():
            url = self.request.route_path('service', service=program.service.slug)
            anchor = "#p%s" % program.anchor
            time = 'läuft' if program.is_running else smartdate(program.start)
            data.append({
                'name': program.name,
                'service': program.service.name,
                'start': time,
                'url': url + anchor
            })
        return data
