from flask_restful import Resource
from flask import request
from flask_login import login_required
from services.employees_generator import get_employees, add_employee


class EmployeesResource(Resource):
    @login_required
    def get(self):
        """Получить список всех сотрудников"""
        try:
            employees = get_employees()
            return [{
                'id': e.id,
                'first_name': e.first_name,
                'last_name': e.last_name,
                'surname': e.surname,
                'job_id': e.job_id,
                'phone': e.phone,
                'email': e.email
            } for e in employees], 200
        except Exception as e:
            return {'error': str(e)}, 500

    @login_required
    def post(self):
        """Создать нового сотрудника"""
        data = request.json

        # Проверка обязательных полей
        required_fields = ['first_name', 'last_name', 'email']
        if not all(field in data for field in required_fields):
            return {'error': f'Не хватает обязательных полей: {required_fields}'}, 400

        try:
            new_employee = add_employee(data)
            return {
                'id': new_employee.id,
                'first_name': new_employee.first_name,
                'last_name': new_employee.last_name,
                'surname': new_employee.surname,
                'job_id': new_employee.job_id,
                'phone': new_employee.phone,
                'email': new_employee.email
            }, 201
        except Exception as e:
            return {'error': str(e)}, 500