# -*- encoding: utf-8 -*-

from datetime import datetime
import pytz

from sqlalchemy import Column, ForeignKey, Integer, Text, String, DateTime
from sqlalchemy.ext.hybrid import Comparator, hybrid_property

from pyramid.threadlocal import get_current_registry

from tvhadikode.models import Base

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

    @property
    def is_running(self, when=None):
        """
        Returns True when this program is currently running.
        """
        if when is None:
            when = datetime.now()
        return self.start <= when <= self.end

    @property
    def remaining(self):
        """
        Returns the remaining number of seconds the program will be running.
        Only valid when is_running=True.
        """
        assert self.is_running
        return (self.end - datetime.now()).total_seconds()

    @property
    def time_until(self):
        """
        Returns the time in seconds until the program starts.
        Returns 0 if program.start is in past.
        """
        if self.start <= datetime.now():
            return 0
        return (self.start - datetime.now()).total_seconds()

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
