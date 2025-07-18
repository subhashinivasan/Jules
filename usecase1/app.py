from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

employees = [
    {"id": 1, "name": "John Doe", "position": "Manager"},
    {"id": 2, "name": "Jane Smith", "position": "Developer"}
]
next_id = 3


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/employees', methods=['POST'])
def create_employee():
    global next_id
    data = request.get_json()
    employee = {
        "id": next_id,
        "name": data['name'],
        "position": data['position']
    }
    employees.append(employee)
    next_id += 1
    return jsonify(employee), 201

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    for employee in employees:
        if employee['id'] == employee_id:
            return jsonify(employee)
    return jsonify({"error": "Employee not found"}), 404

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    for employee in employees:
        if employee['id'] == employee_id:
            employee['name'] = data['name']
            employee['position'] = data['position']
            return jsonify(employee)
    return jsonify({"error": "Employee not found"}), 404

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    global employees
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if employee:
        employees.remove(employee)
        return '', 204
    return jsonify({"error": "Employee not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
