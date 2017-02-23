from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Laboratory(Base):
    __tablename__ = 'laboratory'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}


class Workstation(Base):

    __tablename__ = 'workstation'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    laboratory_id = Column(Integer, ForeignKey('laboratory.id'))

    def serialize(self):
        return {'id': self.id, 'name': self.name }