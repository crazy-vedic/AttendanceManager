import './App.css';
import AttendanceApp from "./AttendanceApp.js"
import {Router, Routes, Route, BrowserRouter} from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AttendanceApp />} />
          {/* <Route path="/attendance" element={<Attendance/>} /> */}
        </Routes>
      </BrowserRouter>
    </div>
  );
}
export default App;
