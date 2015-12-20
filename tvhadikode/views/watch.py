# -*- encoding: utf-8 -*-

from pyramid.decorator import reify
from pyramid.view import view_config
from pyramid.response import Response

from tvhadikode.views.base import BaseView
from tvhadikode.utils.dbhelpers import get_by_or_404
from tvhadikode.models import DBSession, Service, Program

from sqlalchemy.orm import joinedload

import xml.etree.ElementTree as ET

class WatchViews(BaseView):

    @reify
    def service(self):
        return get_by_or_404(Service, slug=self.request.matchdict.get('service'))

    def watch_all(self, get_url, filename):
        body = '#EXTM3U tvg-shift=1\n'
        for service in DBSession.query(Service).order_by(Service.name).all():
            logo = self.request.static_path(service.logo_path_opaque)
            if logo.startswith('/'):
                logo = logo[1:]
            body += '#EXTINF:-1 tvg-id="%s" tvg-logo="%s",%s\n' % (service.slug, logo, service.name)
            body += get_url(service) + "\n"
        return self.make_m3u_response(body, filename)

    def build_single_m3u(self, name, url):
        body = "#EXTM3U\n#EXTINF:0,%s\n%s\n" % (self.service.name, url)
        return self.make_m3u_response(body, name)

    def make_m3u_response(self, body, filename):
        return Response(
            bytes(body, "utf-8"),
            content_type="audio/mpegurl",
            content_length=len(bytes(body, "utf-8")),
            content_disposition='attachment; filename="%s.m3u"' % filename,
            content_encoding='binary',
        )

    @view_config(route_name='service.watch.unicast')
    def service_watch_unicast(self):
        return self.build_single_m3u(self.service.slug, self.service.unicast_path)

    @view_config(route_name='service.watch.multicast')
    def service_watch_multicast(self):
        return self.build_single_m3u(self.service.slug, self.service.multicast_path)

    @view_config(route_name='watch.unicast')
    def watch_unicast(self):
        return self.watch_all(lambda service: service.unicast_path, "tv_unicast.m3u")

    @view_config(route_name='watch.multicast')
    def watch_multicast(self):
        return self.watch_all(lambda service: service.multicast_path, "tv_multicast.m3u")

    @view_config(route_name='watch.xmltv')
    def xmltv(self):
        # Build XML
        root = ET.Element('tv')

        for service in DBSession.query(Service).order_by(Service.name).all():
            channel = ET.SubElement(root, 'channel')
            channel.set('id', service.slug)
            name = ET.SubElement(channel, 'display-name')
            name.set('lang', 'de')
            name.text = service.name

        for program in DBSession.query(Program).options(joinedload('service')).order_by(Program.start).all():
            node = ET.SubElement(root, 'programme')
            node.set('start', program.start_utc.strftime('%Y%m%d%H%M00 +0100'))
            node.set('stop', program.end_utc.strftime('%Y%m%d%H%M00 +0100'))
            node.set('channel', program.service.slug)
            title = ET.SubElement(node, 'title')
            title.set('lang', 'de')
            title.text = program.name
            if program.caption and len(program.caption) > 0:
                subtitle = ET.SubElement(node, 'sub-title')
                subtitle.set('lang', 'de')
                subtitle.text = program.caption
            if program.description and len(program.description) > 0:
                desc = ET.SubElement(node, 'desc')
                desc.set('lang', 'de')
                desc.text = program.description

        # Render XML
        body = b'<?xml version="1.0" encoding="utf-8" ?>\n'
        body += ET.tostring(root, encoding="utf-8")

        # Return HTTP response
        return Response(
            body,
            content_type="application/xml",
            content_length=len(body),
            content_disposition='attachment; filename="xmltv.xml"',
            content_encoding='binary',
        )
