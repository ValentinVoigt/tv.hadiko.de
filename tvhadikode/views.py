from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import DBSession, Service

@view_config(route_name='home', renderer='templates/epg.mak')
def my_view(request):
    services = DBSession.query(Service).all()
    return {'services': services, 'project': 'tv.hadiko.de'}
