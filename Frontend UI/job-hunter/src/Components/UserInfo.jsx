import React, { useState } from 'react';

const Form = () => {
  const [name, setName] = useState('');
  const [degree, setDegree] = useState('');
  const [workExperiences, setWorkExperiences] = useState([{ title: '', description: '' }]);

  const handleAddExperience = () => {
    setWorkExperiences([...workExperiences, { title: '', description: '' }]);
  };

  const handleExperienceChange = (index, key, value) => {
    const newExperiences = [...workExperiences];
    newExperiences[index][key] = value;
    setWorkExperiences(newExperiences);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
    console.log({ name, degree, workExperiences });
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: 'auto' }}>
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="name" style={{ display: 'block', marginBottom: '0.5rem' }}>Name:</label>
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
        <label htmlFor="degree" style={{ display: 'block', marginBottom: '0.5rem' }}>Highest Degree:</label>
        <select
          id="degree"
          value={degree}
          onChange={(e) => setDegree(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        >
          <option value="">Select Degree</option>
          <option value="No Degree">No Degree</option>
          <option value="Undergraduate">Undergraduate</option>
          <option value="Postgraduate">Postgraduate</option>
        </select>
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
