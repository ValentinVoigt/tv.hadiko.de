# -*- encoding: utf-8 -*-

from pyramid.decorator import reify
from pyramid.view import view_config
from pyramid.response import Response

from tvhadikode.views.base import BaseView
from tvhadikode.utils.dbhelpers import get_by_or_404
from tvhadikode.models import Service

class WatchViews(BaseView):

    @reify
    def service(self):
        return get_by_or_404(Service, slug=self.request.matchdict.get('service'))

    @view_config(route_name='channel.watch.unicast')
    def watch_unicast(self):
        return self.return_m3u(self.service.slug, self.service.unicast_url)

    @view_config(route_name='channel.watch.multicast')
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
