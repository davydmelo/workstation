from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Laboratory, Workstation, getBase

app = Flask(__name__)
api = Api(app)

engine = create_engine('sqlite:///workstation.db')

getBase().metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind = engine) 

class LaboratoryListResource(Resource):
	def get(self): #ok
		session = Session()
		labs = session.query(Laboratory).all()
		return jsonify(laboratories = [l.serialize() for l in labs])		
		
	def post(self): #ok
		session = Session()
		parser = reqparse.RequestParser()
		
		parser.add_argument('id', type=int, required=False, location='json')
		parser.add_argument('name', type=str, required=True, location='json')
		parser.add_argument('description', type=str, required=False, location='json')
		
		args = parser.parse_args(strict=True)
		
		laboratory = Laboratory(id = args['id'], name = args['name'], description = args['description'])

		session.add(laboratory)
		session.commit()
		
		return laboratory.serialize()

class LaboratoryResource(Resource):
	def get(self, lid): #ok
		session = Session()
		laboratory = session.query(Laboratory).filter(Laboratory.id == lid).first()

		if not laboratory:
			return {'message' : 'No laboratory found.'}
			
		return laboratory.serialize()
		
	def delete(self, lid): #ok
		session = Session()
		laboratory = session.query(Laboratory).filter(Laboratory.id == lid).first()

		if not laboratory:
			return {'message' : 'No laboratory found.'}

		session.delete(laboratory)
		session.commit()

		return {'message': 'Success.'}
	
	def put(self, lid): #ok
		session = Session()
		laboratory = session.query(Laboratory).filter(Laboratory.id == lid).first()

		parser = reqparse.RequestParser()

		parser.add_argument('name', type=str, required=True, location='json')
		parser.add_argument('description', type=str, required=True, location='json')

		args = parser.parse_args()

		laboratory.name = args['name']
		laboratory.description = args['description']

		session.add(laboratory)
		session.commit()

		return laboratory.serialize(), 201
		
class WorkstationResource(Resource):
	def get(self, lid,  wid): #ok
		session = Session()
		workstation = session.query(Workstation).filter(and_(Workstation.laboratory_id == lid, Workstation.id == wid)).first()

		if not workstation:
			return {'message' : 'No workstation found.'}

		return workstation.serialize()
		
	def delete(self, lid, wid): #ok
		session = Session()
		workstation = session.query(Workstation).filter(and_(Workstation.laboratory_id == lid, Workstation.id == wid)).first()

		if not workstation:
			return {'message' : 'No workstation found.'}

		session.delete(workstation)
		session.commit()

		return {'message': 'Success.'}

	def put(self, lid, wid): #ok
		session = Session()
		workstation = session.query(Workstation).filter(and_(Workstation.laboratory_id == lid, Workstation.id == wid)).first()

		parser = reqparse.RequestParser()

		parser.add_argument('name', type=str, required=True, location='json')

		args = parser.parse_args()

		workstation.name = args['name']

		session.add(workstation)
		session.commit()

		return workstation.serialize(), 201
		
class WorkstationListResource(Resource):
	def get(self, lid): #ok
		session = Session()

		workstations = session.query(Workstation).filter(Workstation.laboratory_id == lid).all()
		
		if not workstations:
			return {'message' : 'No workstations found.'}
		
		return jsonify(workstations = [l.serialize() for l in workstations])
		
	def post(self, lid): #ok
		session = Session()
		parser = reqparse.RequestParser()

		parser.add_argument('name', type=str, required=True, location='json')

		# TODO checar a existência dos parâmetros no JSON
		args = parser.parse_args()

		laboratory = session.query(Laboratory).filter(Laboratory.id == lid).first()

		if not laboratory:
			return {'message' : 'No laboratory found.'}

		workstation =  Workstation(name = args['name'])

		# TODO checar se já não existe esta workstation
		laboratory.workstations.append(workstation)

		session.add(laboratory)
		session.commit()

		return {"message" : "Sucess."}
		

api.add_resource(LaboratoryListResource, '/reservation/laboratory/')
api.add_resource(LaboratoryResource, '/reservation/laboratory/<lid>')
api.add_resource(WorkstationListResource, '/reservation/laboratory/<lid>/workstation/')
api.add_resource(WorkstationResource, '/reservation/laboratory/<lid>/workstation/<wid>')

if __name__ == '__main__':
	app.run(debug = True)