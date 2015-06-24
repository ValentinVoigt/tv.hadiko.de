# -*- encoding: utf-8 -*-

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from tvhadikode.views.base import BaseView

class ErrorViews(BaseView):

    @view_config(context=HTTPNotFound, renderer='tvhadikode:templates/errors/404.mak')
    def not_found(self):
        self.request.response.status = 404
        return {}
