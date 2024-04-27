import React from 'react';
import { useLocation } from 'react-router-dom';
import './DisplayJobs.css'; // Import CSS file for styling
const DisplayJobs = () => {
  const { state } = useLocation();
  const jobData = state?.jobData?.recommended_jobs || []; // Ensure jobData is defined and has recommended_jobs array

  return (
    <div className="jobs-container">
        <h1 className="jobs-heading">Recommended Jobs</h1>
        <div className="jobs-list">
            {jobData.map(job => (
            <div key={job.Job_id} className="job-item">
                <p><strong>Job ID:</strong> {job.job_id}</p>
                <p><strong>Job Title:</strong> {job.job_title}</p>
                <p><strong>Job Description:</strong> {job.job_description.slice(0, 500)}</p>
            </div>
            ))}
        </div>
    </div>
  );
};

export default DisplayJobs;
