from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Workstation(Base):

    __tablename__ = 'workstation'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    laboratory_id = Column(Integer, ForeignKey('laboratory.id'))
    laboratory = relationship("Laboratory", back_populates="workstations")

    def serialize(self):
        return {'id': self.id, 'name': self.name }


class Laboratory(Base):

    __tablename__ = 'laboratory'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    workstations = relationship("Workstation", order_by = Workstation.id, back_populates = "laboratory")

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

def getBase():
    return Base

