# -*- encoding: utf-8 -*-

from datetime import datetime

from pyramid.view import view_config
from pyramid.renderers import render

from sqlalchemy import and_
from sqlalchemy.orm import aliased

from tvhadikode.models import DBSession, Service, Program
from tvhadikode.views.base import BaseView

class HomeViews(BaseView):

    def build_query(self):
        now = datetime.now()
        current = aliased(Program)
        next_ = aliased(Program)

        services = DBSession.query(Service, current, next_)
        services = services.outerjoin(current, and_(current.sid==Service.sid, current.start<=now, current.end>=now))
        services = services.outerjoin(next_, and_(next_.id==current.next_program_id, current.start<=now, current.end>=now))
        return services.order_by(Service.name)

    @view_config(route_name='home', renderer='tvhadikode:templates/epg.mak')
    def epg(self):
        return {'services': self.build_query().all()}

    @view_config(route_name='ajax.epg_update', renderer="json")#, request_method="POST")
    def epg_update(self):
        slugs = self.request.POST.getall('services[]')
        if len(slugs) == 0:
            return {'rows': {}}

        service = self.build_query().filter(Service.slug.in_(slugs))
        rows = {}
        for result in service.order_by(Service.name).all():
            service, current_program, next_program = result
            rows[service.slug] = render('tvhadikode:templates/ajax/epgrow.mak', {
                'request': self.request,
                'service': service,
                'current_program': current_program,
                'next_program': next_program,
            })
        return {'rows': rows}
