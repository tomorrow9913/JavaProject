# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Table, Text, text
from sqlalchemy.sql.sqltypes import NullType, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Menu(Base):
    __tablename__ = 'Menu'

    name = Column(Text, primary_key=True)
    category = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    suggestion = Column(Integer, server_default=text("NULL"))
    thumbnail_url = Column(Integer)


class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    order_time = Column(DateTime, nullable=False, server_default=text("TIMESTAMP"))
    progress = Column(Integer, nullable=False, server_default=text("0"))


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    role = Column(Text, nullable=False, server_default=text("' '"))


class OrderMenu(Base):
    __tablename__ = 'Order_menu'

    order_id = Column(ForeignKey('Order.id'), primary_key=True)
    order_menu = Column(ForeignKey('Menu.name'), primary_key=True)
    order_cnt = Column(Integer)

    order = relationship('Order')
    Menu = relationship('Menu')
