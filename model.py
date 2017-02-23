from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    reg_number = Column(Integer)
    is_admin = Column(Boolean)

    def is_username_valid(self):
        return len(self.username) >= 6

class Vendor(Base):

    __tablename__ = 'vendor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    materials = relationship("Material", back_populates="vendor")

class Material(Base):

    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    name = Column(String)
    model = Column(String)

    vendor_id = Column(Integer, ForeignKey('vendor.id'))
    vendor = relationship("Vendor", back_populates="materials")

    def is_username_valid(self):
        return len(self.username) >= 6

class Reservation(Base):

    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    begin = Column(DateTime)
    end = Column(DateTime)

    workstation_id = Column(Integer, ForeignKey('workstation.id'))
    workstation = relationship("Workstation", back_populates="reservations")

    def serialize(self):
        return {"id": self.id, "begin": self.begin, "end": self.end}


class Workstation(Base):

    __tablename__ = 'workstation'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    laboratory_id = Column(Integer, ForeignKey('laboratory.id'))
    laboratory = relationship("Laboratory", back_populates="workstations")

    reservations = relationship("Reservation", order_by=Reservation.id, back_populates="workstation")

    def serialize(self):
        return {'id': self.id, 'name': self.name, "reservations" : [r.serialize() for r in self.reservations]}


class Laboratory(Base):

    __tablename__ = 'laboratory'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    workstations = relationship("Workstation", order_by = Workstation.id, back_populates = "laboratory")

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, "workstations" : [w.serialize() for w in self.workstations]}

def getBase():
    return Base

