import logo from './logo.svg';
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import HomePage from './Components/HomePage';
import DisplayJobs from './Components/DisplayJobs';
import Header from './Components/Header';
import Footer from './Components/Footer';

function App() {
  return (
    <div>
      <Header />
        <Routes>
          <Route exact path="/" element={<HomePage/>} />
          <Route exact path="/jobs" element={<DisplayJobs/>} />
        </Routes>
      <Footer teamMembers={[['Piyush Sharan', 'Manisha Panda'], ['Neha Manghnani', 'Janvita Reddy']]} />
    </div>

    
  );
}

export default App;
