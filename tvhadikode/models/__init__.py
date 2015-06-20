# -*- encoding: utf-8 -*-

from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.inspection import inspect

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    """ Base model for all models.
    """
    __abstract__ = True

    @classmethod
    def get(cls, *args):
        """ Returns object by primary ID.
        Returns None if object is not found.
        """
        primary_keys = [i.key for i in inspect(cls).primary_key]
        filter_ = dict(zip(primary_keys, args))
        return DBSession.query(cls).filter_by(**filter_).first()

    @classmethod
    def get_by(cls, **kwargs):
        """ Returns the first object by given filter.
        Returns None if object is not found.
        """
        return DBSession.query(cls).filter_by(**kwargs).first()

from .program import Program
from .service import Service

__all__ = ["DBSession", "Program", "Service"]
