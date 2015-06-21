# -*- encoding: utf-8 -*-

import os

from datetime import datetime, timedelta

from sqlalchemy import and_, Column, Integer, String
from sqlalchemy.orm import relationship, reconstructor

from pyramid.path import AssetResolver

from tvhadikode.models import Base, Program

def join_current():
    now = datetime.now()
    return and_(Program.sid==Service.sid, Program.start<=now, Program.end>=now)

def join_next():
    return and_(Program.id==Service.current_program.next_program_id)

def join_future():
    now = datetime.now()
    return and_(Program.sid==Service.sid, Program.end>=now)

class TimedRelationCache:

    _cache = None
    _time = ""
    _model = None
    _attribute = None

    def __init__(self, model, attribute):
        self._model = model
        self._attribute = attribute

    def get(self):
        now = datetime.now().strftime("%H%M")
        if now != self._time:
            self._cache = getattr(self._model, self._attribute)
            self._time = now
        return self._cache

class Service(Base):
    """
    Represents a DVB service. (i.e. a TV channel)
    """
    __tablename__ = 'services'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)
    sid = Column(Integer, nullable=False, unique=True) # Service ID
    name = Column(String(255), index=True, nullable=False)
    slug = Column(String(255), nullable=False)
    multicast_ip = Column(String(255), nullable=False)
    unicast_url = Column(String(255), nullable=False)

    programs = relationship("Program", backref="service", order_by="Program.start")

    current_program = relationship("Program", lazy="joined", bake_queries=False, viewonly=True, uselist=False, join_depth=3, primaryjoin=join_current)
    future_programs_raw = relationship("Program", bake_queries=False, viewonly=True, primaryjoin=join_future, order_by=Program.start_utc)
    future_programs_cached = None

    @reconstructor
    def init_on_load(self):
        self.future_programs_cached = TimedRelationCache(self, 'future_programs_raw')

    @property
    def future_programs(self):
        return self.future_programs_cached.get()

    @property
    def next_program(self):
        return self.current_program.next

    @property
    def logo_path(self):
        return "tvhadikode:static/services/%i.png" % self.sid

    @property
    def has_logo(self):
        path = AssetResolver().resolve(self.logo_path).abspath()
        return os.path.isfile(path)
