# -*- encoding: utf-8 -*-

from pyramid.decorator import reify
from pyramid.view import view_config
from pyramid.response import Response

from tvhadikode.views.base import BaseView
from tvhadikode.utils.dbhelpers import get_by_or_404
from tvhadikode.models import DBSession, Service

class WatchViews(BaseView):

    @reify
    def service(self):
        return get_by_or_404(Service, slug=self.request.matchdict.get('service'))

    @view_config(route_name='service.watch.unicast')
    def service_watch_unicast(self):
        return self.build_single_m3u(self.service.slug, self.service.unicast_path)

    @view_config(route_name='service.watch.multicast')
    def service_watch_multicast(self):
        return self.build_single_m3u(self.service.slug, self.service.multicast_path)

    def watch_all(self, get_url, filename):
        body = '#EXTM3U tvg-shift=1\n'
        for service in DBSession.query(Service).order_by(Service.name).all():
            logo = self.request.static_path(service.logo_path)
            body += '#EXTINF:-1 tvg-id="%s" tvg-logo="%s",%s\n' % (service.slug, logo, service.name)
            body += get_url(service) + "\n"
        return self.make_m3u_response(body, filename)

    @view_config(route_name='watch.unicast')
    def watch_unicast(self):
        return self.watch_all(lambda service: service.unicast_path, "tv_unicast.m3u")

    @view_config(route_name='watch.multicast')
    def watch_multicast(self):
        return self.watch_all(lambda service: service.multicast_path, "tv_multicast.m3u")

    def build_single_m3u(self, name, url):
        body = "#EXTM3U\n#EXTINF:0,%s\n%s" % (self.service.name, url)
        return self.make_m3u_response(body, name)

    def make_m3u_response(self, body, filename):
        return Response(
            bytes(body, "utf-8"),
            content_type="audio/mpegurl",
            content_length=len(body),
            content_disposition='attachment; filename="%s.m3u"' % filename,
            content_encoding='binary',
        )
