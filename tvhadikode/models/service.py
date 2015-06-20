# -*- encoding: utf-8 -*-

import os

from datetime import datetime

from sqlalchemy import and_, Column, Integer, String
from sqlalchemy.orm import relationship

from pyramid.path import AssetResolver

from tvhadikode.models import Base, Program

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

    @property
    def current_program(self):
        if len(self.future_programs) == 0:
            return None
        if not self.future_programs[0].is_running():
            return None
        return self.future_programs[0]

    @property
    def logo_path(self):
        return "tvhadikode:static/services/%i.png" % self.sid

    @property
    def has_logo(self):
        path = AssetResolver().resolve(self.logo_path).abspath()
        return os.path.isfile(path)
