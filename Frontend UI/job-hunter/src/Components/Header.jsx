import React from 'react';

const Header = () => {
  return (
    <header style={{ backgroundColor: '#f0f0f0', padding: '1rem', marginBottom: '1rem', textAlign: 'center' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <img src="../logo.svg" alt="JobHunter Logo" style={{ width: '50px', marginRight: '1rem' }} />
        <h1 style={{ margin: 0 }}>JobHunter</h1>
      </div>
      <p style={{ marginTop: '0.5rem', fontSize: '1.1rem' }}>
        Welcome to JobHunter, your one-stop destination for finding the perfect job opportunities.
      </p>
    </header>
  );
};

export default Header;
