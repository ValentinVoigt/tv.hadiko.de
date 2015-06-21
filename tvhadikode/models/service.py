# -*- encoding: utf-8 -*-

import os

from datetime import datetime

from sqlalchemy import select, and_, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from pyramid.path import AssetResolver

from tvhadikode.models import DBSession, Base, Program

def join_future():
    now = datetime.now()
    return and_(Program.sid==Service.sid, Program.end>=now)

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

    future_programs= relationship("Program", viewonly=True, primaryjoin=join_future, order_by=Program.start_utc)

    def __repr__(self):
        return '<Service name="%s">' % self.name

    @property
    def logo_path(self):
        return "tvhadikode:static/services/%i.png" % self.sid

    @property
    def has_logo(self):
        path = AssetResolver().resolve(self.logo_path).abspath()
        return os.path.isfile(path)
