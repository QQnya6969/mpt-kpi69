import collections
import random

Employee = collections.namedtuple('Employee', 'id first_name last_name surname job_id phone email'.split())

# Мок-данные для разработки
employees_list = [
    Employee(
        id=1,
        first_name="Иван",
        last_name="Иванов",
        surname="Иванович",
        job_id=1,
        phone="+79990001122",
        email="ivan@example.com"
    ),
    Employee(
        id=2,
        first_name="Петр",
        last_name="Петров",
        surname="Петрович",
        job_id=1,
        phone="+79990003344",
        email="petr@example.com"
    )
]

def get_employees():
    """Возвращает список всех сотрудников"""
    return employees_list

def add_employee(employee_data):
    """Добавляет нового сотрудника в список"""
    new_id = max(e.id for e in employees_list) + 1 if employees_list else 1
    employee = Employee(
        id=new_id,
        first_name=employee_data['first_name'],
        last_name=employee_data['last_name'],
        surname=employee_data.get('surname', ''),
        job_id=employee_data.get('job_id', 1),
        phone=employee_data.get('phone', ''),
        email=employee_data['email']
    )
    employees_list.append(employee)
    return employee