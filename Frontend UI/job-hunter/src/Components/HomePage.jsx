import React, { useState } from 'react';
import Form from './UserInfo'
import Header from './Header';
import Footer from './Footer';

const HomePage = () => {
    return (
        <div className="App">
            <div className="form-container">
              <Form />
            </div>
        </div>
    );
};

export default HomePage;