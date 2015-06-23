# -*- encoding: utf-8 -*-

import os

from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from pyramid.path import AssetResolver
from pyramid.decorator import reify

from tvhadikode.models import DBSession, Base, Program

class Service(Base):
    """
    Represents a DVB service. (i.e. a TV channel)
    """
    __tablename__ = 'services'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)
    sid = Column(Integer, nullable=False, unique=True) # Service ID
    name = Column(String(255), index=True, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    multicast_ip = Column(String(255), nullable=False)
    unicast_url = Column(String(255), nullable=False)

    programs = relationship("Program", backref="service", order_by="Program.start")

    def __repr__(self):
        return '<Service name="%s">' % self.name

    @reify
    def future_programs(self):
        now = datetime.now()
        query = DBSession.query(Program).filter(Program.sid==self.sid, Program.end>=now)
        query = query.order_by(Program.start_utc)
        return query.all()

    @property
    def logo_path(self):
        return "tvhadikode:static/services/%i.png" % self.sid

    @property
    def has_logo(self):
        path = AssetResolver().resolve(self.logo_path).abspath()
        return os.path.isfile(path)
