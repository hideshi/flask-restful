from flask import Flask, jsonify, request, abort, make_response
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy, SignallingSession, orm
from dataclasses import dataclass

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restapi.db'
db = SQLAlchemy(app)

@dataclass
class Employee(db.Model):
    __tablename__ = 'employee'

    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

@app.get('/employees')
def get_employees():
    try:
        employees = Employee.query.all()
        if len(employees) != 0:
            return jsonify(employees)
        else:
            return make_response(jsonify({'message': 'Not found'}), 404)
    except Exception as e:
        app.logger.error(e)
        return make_response(jsonify({'message': 'Internal server error'}), 500)

@app.get('/employees/<id>')
def get_employee(id):
    try:
        employee = Employee.query.filter(Employee.id == id).first()
        app.logger.info(employee)
        if employee is not None:
            return jsonify(employee)
        else:
            return make_response(jsonify({'message': 'Not found'}), 404)
    except Exception as e:
        app.logger.error(e)
        return make_response(jsonify({'message': 'Internal server error'}), 500)

@app.post('/employees')
def create_employee():
    try:
        name = request.form['name']
        employee = Employee(name=name)
        db.session.add(employee)
        db.session.commit()
        resp = make_response(jsonify({'message': 'Resource has been created'}), 201)
        resp.headers['Location'] = f'{request.scheme}://{request.host}/employees/{employee.id}'
        return resp
    except Exception as e:
        app.logger.error(e)
        return make_response(jsonify({'message': 'Internal server error'}), 500)

@app.put('/employees/<id>')
def update_employee(id):
    try:
        name = request.form['name']
        employee = Employee.query.filter(Employee.id == id).first()
        if employee is not None:
            employee.name = name
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response(jsonify({'message': 'Bad request'}), 400)
    except Exception as e:
        app.logger.error(e)
        return make_response(jsonify({'message': 'Internal server error'}), 500)

@app.patch('/employees/<id>')
def update_employee_partially(id):
    try:
        name = request.form['name']
        employee = Employee.query.filter(Employee.id == id).first()
        if employee is not None:
            employee.name = name
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response(jsonify({'message': 'Bad request'}), 400)
    except Exception as e:
        app.logger.error(e)
        return make_response(jsonify({'message': 'Internal server error'}), 500)

@app.delete('/employees/<id>')
def delete_employee(id):
    try:
        employee = Employee.query.filter(Employee.id == id).first()
        app.logger.info(employee)
        if employee is not None:
            db.session.delete(employee)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response(jsonify({'message': 'Bad request'}), 400)
    except Exception as e:
        app.logger.error(e)
        return make_response(jsonify({'message': 'Internal server error'}), 500)

