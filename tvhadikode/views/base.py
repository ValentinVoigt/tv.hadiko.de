# -*- encoding: utf-8 -*-

class BaseView:

    request = None

    def __init__(self, request):
        self.request = request
