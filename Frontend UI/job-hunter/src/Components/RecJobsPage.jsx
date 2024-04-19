import React from 'react';
import RecommendedJob from './RecommendedJob';

const RecommendedJobPage = ({ jobs }) => {
  return (
    <div>
      <h2>Recommended Jobs</h2>
      {jobs.map((job, index) => (
        <RecommendedJob
          key={index}
          title={job.title}
          description={job.description}
          applyLink={job.applyLink}
        />
      ))}
    </div>
  );
};

export default RecommendedJobPage;
