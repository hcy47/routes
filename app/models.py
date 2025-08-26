from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, String, Table, Column, VARCHAR, Integer, Float
from flask_marshmallow import Marshmallow

#Create a base class for our models
class Base(DeclarativeBase):
    pass
    #could add your own config


#Instatiate your SQLAlchemy database:
db = SQLAlchemy(model_class = Base)



class Customers(Base):
    __tablename__ = 'customers' 

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[VARCHAR] = mapped_column(VARCHAR(120), nullable=False)
    last_name: Mapped[VARCHAR] = mapped_column(VARCHAR(360), unique=True, nullable=False)
    email: Mapped[VARCHAR] = mapped_column(VARCHAR, unique=True,  nullable=False)
    phone: Mapped[VARCHAR] = mapped_column(VARCHAR(30), nullable=False)
    address: Mapped[VARCHAR] = mapped_column(VARCHAR(500), nullable=True)
    

    service_tickets: Mapped[list["Service_tickets"]] = relationship('Service_tickets', back_populates='customers')




class Service_tickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(360), nullable=False)
    price: Mapped[float] = mapped_column(Float(60), nullable=False)
    VIN: Mapped[str] = mapped_column(String(20), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=True)
    

    customers: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')
    mechanics: Mapped[list["Mechanics"]] = relationship('Mechanics', secondary='ticket_mechanics', back_populates='service_tickets')
  



class Mechanics(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[VARCHAR] = mapped_column(VARCHAR(120), nullable=False)
    last_name: Mapped[VARCHAR] = mapped_column(VARCHAR(360), unique=True, nullable=False)
    email: Mapped[VARCHAR] = mapped_column(VARCHAR, unique=True,  nullable=False)
    password: Mapped[VARCHAR] = mapped_column(VARCHAR, unique=True, nullable=False)
    salary: Mapped[float] = mapped_column(Float(360), nullable=False)
    address: Mapped[VARCHAR] = mapped_column(VARCHAR(500), nullable=True)

    service_tickets: Mapped[list['Service_tickets']] = relationship('Service_tickets', secondary='ticket_mechanics', back_populates='mechanics')
    

class Ticket_mechanics(Base):
    __tablename__ = 'ticket_mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('service_tickets.id'), nullable=False)
    mechanic_id: Mapped[int] = mapped_column(ForeignKey('mechanics.id'), nullable=False)

