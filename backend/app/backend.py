# backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from initiate import retrieve_connection, execute_query
import logging

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Check Attendance for a student
@app.route('/check-attendance', methods=['GET'])
@cross_origin()
def check_attendance():
    student_id = request.args.get('id','*',type=str)

    if not student_id:
        return jsonify({"error": "Missing id parameter"}), 400
    if student_id=='*': query = "SELECT student_id,student_name,attendance FROM Students LIMIT 100"
    else: query = "SELECT student_id,student_name, attendance FROM Students WHERE student_id = %s"
    try:
        connection = retrieve_connection()
        if student_id=='*': result = execute_query(connection, query)
        else: result = execute_query(connection, query, (student_id,))
        if result:
            if student_id == '*':
                attendance_list = [
                    {"student_id":row[0],"student_name": row[1], "attendance": row[2]}
                    for row in result
                ]
                return jsonify(attendance_list), 200
            else:
                # Return single student data if a specific ID is queried
                student_id, student_name, attendance = result[0]
                return jsonify({"student_id": student_id, "student_name": student_name, "attendance": attendance}), 200
        else:
            return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching attendance: {e}")
        return jsonify({"error": str(e)}), 500

# Mark Attendance for a student
@app.route('/mark-attendance', methods=['POST'])
@cross_origin()
def mark_attendance():
    """
    Mark attendance for a student, ensuring one IP can only mark once after a restart.
    """
    data = request.json
    student_id = data.get('id')

    if not student_id:
        return jsonify({"error": "Missing id"}), 400

    ip_address = request.remote_addr  # Get IP address of the client

    try:
        with retrieve_connection() as connection:
            # Check if the IP has already marked attendance
            ip_check_query = "SELECT * FROM AttendanceIP WHERE ip_address = %s;"
            result = execute_query(connection, ip_check_query, (ip_address,))
            if result:
                return jsonify({"error": "Attendance already marked from this IP"}), 403

            # Mark attendance for the student
            mark_query = "UPDATE Students SET attendance = 1 WHERE student_id = %s;"
            execute_query(connection, mark_query, (student_id,))
            
            # Insert the IP address into AttendanceIP table
            insert_ip_query = "INSERT INTO AttendanceIP (ip_address) VALUES (%s);"
            execute_query(connection, insert_ip_query, (ip_address,))
            
            return jsonify({"message": "Attendance marked successfully"}), 200

    except Exception as e:
        logging.error(f"Failed to mark attendance: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
