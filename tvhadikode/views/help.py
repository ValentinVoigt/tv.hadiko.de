# -*- encoding: utf-8 -*-

from pyramid.view import view_config

from tvhadikode.views.base import BaseView

class HelpViews(BaseView):

    @view_config(route_name='help', renderer='tvhadikode:templates/help.mak')
    def help(self):
        return {}
