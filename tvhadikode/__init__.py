# -*- encoding: utf-8 -*-

import locale

from pyramid.config import Configurator
from pyramid.settings import asbool
from sqlalchemy import engine_from_config
from paste.translogger import TransLogger

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    assert 'tv.static_path' in settings
    assert 'tv.locale' in settings
    assert 'tv.timezone' in settings
    assert 'tv.unicast_host' in settings
    assert 'tv.mumudvb_urls' in settings

    locale.setlocale(locale.LC_ALL, settings.get('tv.locale'))

    config.include('pyramid_mako')

    config.add_static_view(settings.get('tv.static_path'), 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('help', '/help')
    config.add_route('status', '/status')
    config.add_route('service', '/services/{service}')
    config.add_route('watch.multicast', '/playlist/tv_multicast.m3u')
    config.add_route('watch.unicast', '/playlist/tv_unicast.m3u')
    config.add_route('watch.xmltv', '/playlist/xmltv.xml')
    config.add_route('service.watch.multicast', '/services/{service}/multicast.m3u')
    config.add_route('service.watch.unicast', '/services/{service}/unicast.m3u')

    config.add_route('ajax.epg_update', '/ajax/epg-update')
    config.add_route('ajax.status.traffic', '/ajax/status/traffic')
    config.add_route('ajax.status.signal_clients', '/ajax/status/signal_clients')
    config.add_route('ajax.search.services', '/ajax/search/services')
    config.add_route('ajax.search.programs', '/ajax/search/programs/{query}')

    config.scan()

    app = config.make_wsgi_app()
    app = TransLogger(app, setup_console_handler=False)
    return app
