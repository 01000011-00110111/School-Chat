// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React from "react";
import Offline from "./pages/Offline";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Outlet,
    Navigate,
    useLocation,
} from "react-router-dom";
import Settings from './pages/Settings';
import Chat from './pages/Chat';
import Login from './pages/Login';
function App() {
    function ProtectedRoute({ isAuthenticated, redirectPath = '/login', children }) {
        const location = useLocation();
      
        if (!isAuthenticated) {
          // Redirect to the login page if not authenticated
          return <Navigate to={redirectPath} state={{ from: location }} replace />;
        }
      
        // Render the children (the protected route content) if authenticated
        return children ? children : <Outlet />;
    }
      
    return (
        <Router>
            <Routes>
              <Route path='/' element={<Login/>}/>  
              <Route path='/chat' element={<Chat/>}/>
              {/* <Route path='/chat/:id' element={<Chat/>}/> */}
              <Route path='/settings' element={<Settings/>}/>
              <Route path="/login" element={<Login/>}/>
            </Routes>
        </Router>
    );
}

export default App;