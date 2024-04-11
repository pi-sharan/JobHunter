import logo from './logo.svg';
import './App.css';
import Form from './Components/UserInfo'
import Header from './Components/Header';
import Footer from './Components/Footer';

function App() {
  return (
    <div className="App">
        <Header />
        <div className="form-container">
          <Form />
        </div>
        <Footer teamMembers={[['Piyush Sharan', 'Manisha Panda'], ['Neha Manghnani', 'Janvita Reddy']]} />
    </div>
  );
}

export default App;
