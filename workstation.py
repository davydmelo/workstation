from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model import Laboratory, Workstation

app = Flask(__name__)
api = Api(app)

Base = declarative_base()
engine = create_engine('sqlite:///workstation.db')

Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind = engine) 

laboratory_db = [
	{
		'id' : '1',
		'name' : 'Laboratório 03',
		'description' : 'Laboratório destinado às práticas de circuitos elétrico e eletrônicos.',
		'workstations' : [
			{ 'id': '1', 'name' : 'Baia 1' },
			{ 'id': '2', 'name' : 'Baia 2' },
			{ 'id': '3', 'name' : 'Baia 3' }
		]
	},
	{
		'id' : '2',
		'name' : 'Laboratório 04',
		'description' : 'Laboratório destinado às práticas de projeto lógico digital e sistemas embarcados.',
		'workstations' : [
			{ 'id': '4', 'name' : 'Baia 1' },
			{ 'id': '5', 'name' : 'Baia 2' },
			{ 'id': '6', 'name' : 'Baia 3' },
			{ 'id': '7', 'name' : 'Baia 4' },
		]
	}
]

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
		lab = [lab for lab in laboratory_db if (lab['id'] == lid)]
		
		if not lab:
			return {'message' : 'No laboratory found.'}
			
		workstations = lab[0]['workstations']
		wst = [wst for wst in workstations if (wst['id'] == wid)]
		
		if not wst:
			return {'message' : 'No workstation found.'}
		
		return wst[0]
		
	def delete(self):
		pass
		
	def put(self):
		pass
		
class WorkstationListResource(Resource):
	def get(self, lid): #ok
		lab = [lab for lab in laboratory_db if (lab['id'] == lid)]
		
		if not lab:
			return {'message' : 'No laboratory found.'}
		
		return lab[0]['workstations']
		
	def post(self, lid): #ok
		lab = [lab for lab in laboratory_db if (lab['id'] == lid)]
		
		if not lab:
			return {'message' : 'No laboratory found.'}
		
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, location='json')
		args = parser.parse_args(strict=True)
		
		workstation = {'name': args['name']}
		
		if workstation in lab[0]['workstations']:
			return {}

		lab[0]['workstations'].append(workstation)
		
		return {"message" : "Sucess."}
		

api.add_resource(LaboratoryListResource, '/reservation/laboratory/')
api.add_resource(LaboratoryResource, '/reservation/laboratory/<lid>')
api.add_resource(WorkstationListResource, '/reservation/laboratory/<lid>/workstation/')
api.add_resource(WorkstationResource, '/reservation/laboratory/<lid>/workstation/<wid>')

if __name__ == '__main__':
	app.run(debug = True)