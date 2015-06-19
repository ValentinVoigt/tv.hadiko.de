from pyramid.response import Response
from pyramid.view import view_config
from pyramid.decorator import reify

from sqlalchemy.exc import DBAPIError

from .utils.dbhelpers import get_by_or_404
from .models import DBSession, Service

class BaseView:

    def __init__(self, request):
        self.request = request

@view_config(route_name='home', renderer='templates/epg.mak')
def my_view(request):
    services = DBSession.query(Service).all()
    return {'services': services, 'project': 'tv.hadiko.de'}

class WatchViews(BaseView):

    @reify
    def service(self):
        return get_by_or_404(Service, slug=self.request.matchdict.get('service'))

    @view_config(route_name='watch.unicast')
    def watch_unicast(self):
        return self.return_m3u(self.service.slug, self.service.unicast_url)

    @view_config(route_name='watch.multicast')
    def watch_multicast(self):
        return self.return_m3u(self.service.slug, "udp://@" + self.service.multicast_ip)

    def return_m3u(self, name, url):
        body = "#EXTM3U\n#EXTINF:0,%s\n%s" % (self.service.name, url)
        return Response(
            bytes(body),
            content_type="audio/mpegurl",
            content_length=len(body),
            content_disposition='attachment; filename="%s.m3u"' % name,
            content_encoding='binary',
        )
