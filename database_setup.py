#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()



class Pages(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    url = Column(String(250), nullable=False)
    status = Column(String(30), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.reqid,
            'status': self.status,
        }

class Requests(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    reqid = Column(String(250), nullable=False)
    start = Column(String(250), nullable=False)
    stop = Column(String(250), nullable=False)
    baseurl = Column(String(250), nullable=False)
    cod = Column(String(250), nullable=False)
    message = Column(String(250), nullable=False)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'reqid': self.reqid,
            'start':self.start,
            'stop': self.stop,
            'baseurl': self.baseurl,
            'cod': self.cod,
            'message': self.message,

        }

class UTCBTC(Base):
    __tablename__ = 'utc_btc'
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    start = Column(String(50), nullable=False)
    stop = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    low = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    open = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    request_date = Column(String(255), nullable=False)
    request_id = Column(Integer, ForeignKey('requests.id'))
    requests = relationship(Requests)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'request_date':self.request_date,
            'start': self.start,
            'stop': self.stop,
            'status': self.status,
            'time': self.time,
            'low': self.low,
            'high': self.high,
            'open': self.open,
            'close': self.close,
            'volume': self.volume,
            'change': self.change,
            'requests': self.request_id,

        }



engine = create_engine('sqlite:///btc.db')
Base.metadata.create_all(engine)
