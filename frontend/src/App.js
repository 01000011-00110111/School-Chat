// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React, { useEffect, useState } from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    NavLink,
} from "react-router-dom";
import Settings from './pages/Settings';
import Chat from './pages/Chat';
import Login from './pages/Login';
import socket from './socket'

function App() {
    return (
        <Router>
            <Routes>
              <Route path='/' element={<Login/>}/>  
              <Route path='/chat' element={<Chat/>}/>
              <Route path='/settings' element={<Settings/>}/>
            </Routes>
        </Router>
    );
}

export default App;