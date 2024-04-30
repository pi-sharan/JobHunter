import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Form = () => {
  const [name, setName] = useState('');
  const [major, setMajor] = useState('');
  const [degree, setDegree] = useState('');
  const [workExperiences, setWorkExperiences] = useState([{ title: '', description: '' }]);

  const [yearsOfExp, setYearsOfExp] = useState('');
  const [currentlyEmployed, setCurrentlyEmployed] = useState('');
  const [managedOthers, setManagedOthers] = useState('');
  const [managedHowMany, setManagedHowMany] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const navigate = useNavigate();


  const handleAddExperience = () => {
    setWorkExperiences([...workExperiences, { title: '', description: '' }]);
  };

  const handleExperienceChange = (index, key, value) => {
    const newExperiences = [...workExperiences];
    newExperiences[index][key] = value;
    setWorkExperiences(newExperiences);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let workHistory = ""
    for (let i = 0; i < workExperiences.length; i++) {
      workHistory += workExperiences[i].title + ' ';
    }
    let workHistoryCount = (workExperiences.length);

    const formData = {
      major,
      degree,
      workHistoryCount,
      yearsOfExp,
      managedHowMany,
      currentlyEmployed,
      managedOthers,
      city,
      state,
      workHistory,
    };

    console.log(JSON.stringify(formData));

    // Make POST request to Django API
    const response = await axios.post('http://127.0.0.1:8000/api/recommend/', JSON.stringify(formData), {
      headers: {
        'Content-Type': 'application/json' // specifying JSON content
      }
    },
    );
  

    console.log(response.data['recommended_jobs'][0]);

    // history.push({pathname: '/jobs',  })
    navigate('/jobs', { state: { jobData: response.data } });
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: 'auto' }}>
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="name" style={{ display: 'block', marginBottom: '0.5rem' }}>Name</label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="degree" style={{ display: 'block', marginBottom: '0.5rem' }}>Highest Degree</label>
        <select
          id="degree"
          value={degree}
          onChange={(e) => setDegree(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        >
          <option value="">Select Degree</option>
          <option value="None">No Degree</option>
          <option value="High School">High School</option>
          <option value="Vocational">Vocational</option>
          <option value="Associate's">Associate's</option>
          <option value="Bachelor's">Bachelor's</option>
          <option value="Master's">Master's</option>
          <option value="PhD">PhD</option>
        </select>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="major" style={{ display: 'block', marginBottom: '0.5rem' }}>Major</label>
        <input
          type="text"
          id="major"
          value={major}
          onChange={(e) => setMajor(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>


      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="currentlyEmployed" style={{ display: 'block', marginBottom: '0.5rem' }}>Currently Employed?</label>
        <input
          type="text"
          id="currentlyEmployed"
          value={currentlyEmployed}
          onChange={(e) => setCurrentlyEmployed(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="yearsOfExp" style={{ display: 'block', marginBottom: '0.5rem' }}>Years of Experience:</label>
        <input
          type="text"
          id="yearsOfExp"
          value={yearsOfExp}
          onChange={(e) => setYearsOfExp(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="managedOthers" style={{ display: 'block', marginBottom: '0.5rem' }}>Have you managed others?</label>
        <select
          id="managedOthers"
          value={managedOthers}
          onChange={(e) => setManagedOthers(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        >
          <option value="">Select</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="managedHowMany" style={{ display: 'block', marginBottom: '0.5rem' }}>Managed how many others?</label>
        <input
          type="text"
          id="managedHowMany"
          value={managedHowMany}
          onChange={(e) => setManagedHowMany(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="City" style={{ display: 'block', marginBottom: '0.5rem' }}>City</label>
        <input
          type="text"
          id="City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="State" style={{ display: 'block', marginBottom: '0.5rem' }}>State</label>
        <input
          type="text"
          id="State"
          value={state}
          onChange={(e) => setState(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Past Work Experience:</label>
        {workExperiences.map((experience, index) => (
          <div key={index} style={{ marginBottom: '0.5rem' }}>
            <input
              type="text"
              placeholder="Title"
              value={experience.title}
              onChange={(e) => handleExperienceChange(index, 'title', e.target.value)}
              required
              style={{ width: '100%', padding: '0.5rem' }}
            />
            <textarea
              placeholder="Description"
              value={experience.description}
              onChange={(e) => handleExperienceChange(index, 'description', e.target.value)}
              required
              style={{ width: '100%', padding: '0.5rem', marginTop: '0.5rem' }}
            />
          </div>
        ))}
        <button type="button" onClick={handleAddExperience} style={{ marginTop: '0.5rem' }}>
          Add More
        </button>
      </div>
      <button type="submit" style={{ display: 'block', width: '100%', padding: '0.5rem' }}>Submit</button>
    </form>
  );
};

export default Form;
