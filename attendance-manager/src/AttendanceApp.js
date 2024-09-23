import React, { useState ,useEffect} from 'react';
import axios from 'axios';
import { NavLink } from 'react-router-dom';
import './AttendanceApp.css'

const AttendanceApp = () => {
  const [ip, setIp] = useState(`${window.location.hostname}:5000`);
  const [id, setId] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [attendanceData, setAttendanceData] = useState([]);

  const handleCheckAttendance = async (silent=false) => {
    try {
      let response; // Declare response outside of the if-else block
  
      if (!id) {
        setId('*');
        response = await axios.get(`http://${ip}/check-attendance`, { params: { 'id': '*' } });
      } else {
        response = await axios.get(`http://${ip}/check-attendance`, { params: { id } });
      }
  
      //console.log('Response:', response.data);
  
      if (Array.isArray(response.data)) {
        setAttendanceData(response.data);
      } else {
        setAttendanceData([response.data]); // Handle the case when the response is not an array
      }
      if (!silent){
      setMessage(response.data.message || ''); // Set message or clear
      setError(''); // Clear previous error}
    }} catch (err) {
      console.log('Error:', err);
      setMessage(''); // Clear message on error
      setError(err.response ? err.response.data.message : 'Error connecting to server');
    }
  };
    const handleMarkAttendance = async () => {
    try {
      const response = await axios.post(`http://${ip}/mark-attendance`, { id });
      setMessage(response.data.message || ''); // Set message or clear
      setError(''); // Clear previous error
      handleCheckAttendance(true); // Fetch updated attendance data
    } catch (err) {
      // console.log('Full Error:', err); // Log the full error object for debugging
  
      if (err.response) {
        // If the error has a response, check the status
        if (err.response.data.error){
          setError(err.response.data.error);
        } else if (err.response.data && err.response.data.message) {
          // If error contains a message, use that
          setError(err.response.data.message);
        } else {
          setError(`Error: ${err.response.status}`); // Generic error message with status code
        }
      } else {
        setError('Error connecting to server'); // Handle network or other errors
      }
      
      setMessage(''); // Clear message on error
    }
  };
    const fetchAttendance = async () => {
    try {
      const response = await axios.get(`http://${ip}/check-attendance`,{params: { id: '*' }});
      //console.log(response.data);
      setAttendanceData(response.data);
      setError('');  // Clear any previous error
    } catch (err) {
      setError(err.response ? err.response.data.message : 'Error fetching attendance data');
    }
  };

  useEffect(() => {
    if (ip.length>1)fetchAttendance();
  }, [ip]); // Fetch attendance data when IP changes
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleCheckAttendance(); // Trigger the function on Enter key press
    }
  };

  return (
    <div className="container">
      <NavLink to={"/attendance"}><h2>Attendance System</h2></NavLink>
      <div className="form-group">
        <label>
          Server IP:
          <input type="text" value={ip} onChange={(e) => setIp(e.target.value)} onKeyUp={handleKeyPress} />
        </label>
      </div>
      <div>
        <label>
          ID:
          <input type="text" value={id} onChange={(e) => setId(e.target.value)} onKeyUp={handleKeyPress}/>
        </label>
      </div>
      <button onClick={handleCheckAttendance}>Check Attendance</button>
      <button onClick={handleMarkAttendance}>Mark Attendance</button>
      {message &&<p>Message: {message}</p>}
      {error&&<p className="error">Error: {error}</p>}
      {attendanceData.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Student ID</th>
              <th>Student Name</th>
              <th>Attendance</th>
            </tr>
          </thead>
          <tbody>
            {attendanceData.map((student, index) => (
              <tr key={index}>
                <td>{student.student_id}</td>
                <td>{student.student_name}</td>
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

export default AttendanceApp;
