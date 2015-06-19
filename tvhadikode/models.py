from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

from zope.sqlalchemy import ZopeTransactionExtension

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
    multicast_ip = Column(String(255), nullable=False)
    unicast_url = Column(String(255), nullable=False)
    programs = relationship("Program", backref="service", order_by="Program.start")

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
    start = Column(DateTime, nullable=False, index=True)
    end = Column(DateTime, nullable=False, index=True)
    duration = Column(Integer, nullable=False) # In seconds

    def is_running(self, when=None):
        """
        Returns True when this program is currently running.
        """
        if when is None:
            when = datetime.now()
        return self.start <= when <= self.end
