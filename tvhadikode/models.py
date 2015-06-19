# -*- encoding: utf-8 -*-

from datetime import datetime
import pytz

from sqlalchemy import and_, Column, ForeignKey, Integer, Text, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.hybrid import Comparator, hybrid_property

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.threadlocal import get_current_registry

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

class Service(Base):
    """
    Represents a DVB service. (i.e. a TV channel)
    """
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    sid = Column(Integer, nullable=False, unique=True) # Service ID
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    multicast_ip = Column(String(255), nullable=False)
    unicast_url = Column(String(255), nullable=False)

    programs = relationship("Program", backref="service", order_by="Program.start")

    future_programs = relationship(
        "Program",
        primaryjoin=lambda: and_(Service.sid==Program.sid, Program.end>=datetime.now()),
        order_by="Program.start")

class UTCToLocalComparator(Comparator):

    def __eq__(self, other):
        return self.__clause_element__() == local_to_utc(other)

    def __ge__(self, other):
        return self.__clause_element__() >= local_to_utc(other)

    def __gt__(self, other):
        return self.__clause_element__() > local_to_utc(other)

    def __le__(self, other):
        return self.__clause_element__() <= local_to_utc(other)

    def __lt__(self, other):
        return self.__clause_element__() < local_to_utc(other)

def utc_to_local(dt):
    localtz = pytz.timezone(get_current_registry().settings.get('tv.timezone', pytz.utc))
    return pytz.utc.localize(dt).astimezone(localtz).replace(tzinfo=None)

def local_to_utc(dt):
    localtz = pytz.timezone(get_current_registry().settings.get('tv.timezone', pytz.utc))
    return localtz.localize(dt).astimezone(pytz.utc).replace(tzinfo=None)

class Program(Base):
    """
    Represents an EPG entry.
    """
    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True)
    sid = Column(Integer, ForeignKey('services.sid'), nullable=False) # Service ID
    tid = Column(Integer, nullable=False) # Transportstream ID
    name = Column(String(255), nullable=False)
    language = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    start_utc = Column(DateTime, nullable=False, index=True)
    end_utc = Column(DateTime, nullable=False, index=True)
    duration = Column(Integer, nullable=False) # In seconds

    @hybrid_property
    def start(self):
        return utc_to_local(self.start_utc)

    @start.comparator
    def start(cls):
        return UTCToLocalComparator(cls.start_utc)

    @hybrid_property
    def end(self):
        return utc_to_local(self.end_utc)

    @end.comparator
    def end(cls):
        return UTCToLocalComparator(cls.end_utc)

    def is_running(self, when=None):
        """
        Returns True when this program is currently running.
        """
        if when is None:
            when = datetime.now()
        return self.start <= when <= self.end

    @property
    def percent_complete(self):
        """
        Returns an integer between 0-100.
            0: Program is in past
            1: Program has just started
            50: Program is at half time
            100: Program is over
        """
        def dt_to_unix(dt):
            return int(dt.strftime("%s"))
        now = datetime.now()
        passed = dt_to_unix(now) - dt_to_unix(self.start)
        if passed <= 0:
            return 0
        elif passed > self.duration:
            return 100
        else:
            return round(float(passed) / float(self.duration) * 100)
