import React from 'react';

const RecommendedJob = ({ title, description, applyLink }) => {
  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '5px', padding: '1rem', marginBottom: '1rem' }}>
      <h3>{title}</h3>
      <p>{description}</p>
      <a href={applyLink} target="_blank" rel="noopener noreferrer">Apply Now</a>
    </div>
  );
};

export default RecommendedJob;
