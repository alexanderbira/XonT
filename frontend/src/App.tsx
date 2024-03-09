import React from 'react';
import Form from './Form'
import Evaluation from './Evaluation';
import Results from './Results';

import { connect } from 'socket.io-client';
import { HashRouter, Routes, Route } from "react-router-dom";

import appStyles from './app.module.css';

function App() {
  const socket = connect('http://127.0.0.1:8000/');
  
  return (
    <div className={appStyles.wrapper}>
      <div className={appStyles.content}>
        <HashRouter>
          <Routes>
            <Route path="/" element={<Form />} />
            <Route path="/evaluate-image" element={<Evaluation socket={socket} />} />
            <Route path="/results" element={<Results socket={socket} />} />
          </Routes>
        </HashRouter>
      </div>
    </div>
  );
}

export default App;
