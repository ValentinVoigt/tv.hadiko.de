from pyramid.httpexceptions import HTTPNotFound

def return_or_404(obj, details=""):
    """ Returns an object if obj != None.
    Raises pyramid.httpexceptions.HTTPNotFound if obj is None.
    """
    if details:
        details = " (%s)" % details
    if obj is None:
        raise HTTPNotFound("%s not found%s" % (obj.__class__.__name__, details))
    return obj

def get_or_404(cls, *args):
    """ Uses a model's .get-function to return an object by it's id.
    Raises pyramid.httpexceptions.HTTPNotFound if not found.
    """
    obj = cls.get(*args)
    return return_or_404(obj, str(args))

def get_by_or_404(cls, **kwargs):
    """ Uses a model's .get_by-function to return an object by given filter.
    Raises pyramid.httpexceptions.HTTPNotFound if not found.
    """
    obj = cls.get_by(**kwargs)
    return return_or_404(obj, str(kwargs))
