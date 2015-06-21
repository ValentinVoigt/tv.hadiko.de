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
