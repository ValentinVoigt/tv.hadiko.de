# -*- encoding: utf-8 -*-

from datetime import datetime

from pyramid.view import view_config
from sqlalchemy.orm import aliased

from tvhadikode.models import DBSession, Service, Program
from tvhadikode.views.base import BaseView

class HomeViews(BaseView):

    @view_config(route_name='home', renderer='tvhadikode:templates/epg.mak')
    def epg(self):
        now = datetime.now()
        current = aliased(Program)
        next_ = aliased(Program)
        services = DBSession.query(Service, current, next_)
        services = services.filter(current.sid==Service.sid, current.start<=now, current.end>=now)
        services = services.filter(next_.id==current.next_program_id)
        services = services.order_by(Service.name).all()
        return {'services': services}

    @view_config(route_name='ajax.service.epgrow', renderer='tvhadikode:templates/ajax/epgrow.mak')
    def epgrow(self):
        from time import sleep
        sleep(1)
        now = datetime.now()
        current = aliased(Program)
        next_ = aliased(Program)
        service = DBSession.query(Service, current, next_)
        service = service.filter(Service.slug==self.request.matchdict.get('service'))
        service = service.filter(current.sid==Service.sid, current.start<=now, current.end>=now)
        service = service.filter(next_.id==current.next_program_id)
        service, current_program, next_program = service.order_by(Service.name).one()
        return {
            'service': service,
            'current_program': current_program,
            'next_program': next_program,
        }
