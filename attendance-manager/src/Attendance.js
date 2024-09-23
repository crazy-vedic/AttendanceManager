import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Attendance = () => {
  const [attendanceData, setAttendanceData] = useState([]);
  const [error, setError] = useState('');

  // Function to fetch all attendance data
  const fetchAttendanceData = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/check-attendance`, {
        params: { id: '*' }, // Query all attendance data
      });
      setAttendanceData(response.data);
      setError(''); // Clear error
    } catch (err) {
      setError(err.response ? err.response.data.message : 'Error fetching attendance data');
    }
  };

  // Fetch attendance data when the component mounts
  useEffect(() => {
    fetchAttendanceData();
  }, []);

  return (
    <div>
      <h2>Attendance Information</h2>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {attendanceData.length > 0 ? (
        <table border="1">
          <thead>
            <tr>
              <th>ID</th>
              <th>Attendance</th>
            </tr>
          </thead>
          <tbody>
            {attendanceData.map((student, index) => (
              <tr key={index}>
                <td>{student.student_id}</td>
                <td>{student.attendance}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No attendance data available</p>
      )}
    </div>
  );
};

export default Attendance;
