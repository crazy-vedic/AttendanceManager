import React, { useState } from 'react';
import axios from 'axios';

const AttendanceApp = () => {
  const [ip, setIp] = useState('');
  const [id, setId] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleCheckAttendance = async () => {
    try {
      const response = await axios.get(`http://${ip}/api/check-attendance`, {
        params: { id },
      });
      setMessage(response.data.message);
      setError('');  // Clear any previous error
    } catch (err) {
      setError(err.response ? err.response.data.message : 'Error connecting to server');
    }
  };

  const handleMarkAttendance = async () => {
    try {
      const response = await axios.post(`http://${ip}/api/mark-attendance`, { id });
      setMessage(response.data.message);
      setError('');  // Clear any previous error
    } catch (err) {
      setError(err.response ? err.response.data.message : 'Error connecting to server');
    }
  };

  return (
    <div>
      <h2>Attendance System</h2>
      <div>
        <label>
          Server IP:
          <input type="text" value={ip} onChange={(e) => setIp(e.target.value)} />
        </label>
      </div>
      <div>
        <label>
          ID:
          <input type="text" value={id} onChange={(e) => setId(e.target.value)} />
        </label>
      </div>
      <button onClick={handleCheckAttendance}>Check Attendance</button>
      <button onClick={handleMarkAttendance}>Mark Attendance</button>
      {message && <p>Message: {message}</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
    </div>
  );
};

export default AttendanceApp;
