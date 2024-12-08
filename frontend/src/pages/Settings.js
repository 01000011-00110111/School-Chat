// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React from "react";

const Settings = () => {
    return (
        <div className="settings_page">
            <div className="settings_navigation_container">
                <button>Close</button>
                <button>My Profile</button>
                <button>Account</button>
                <button>Notifications</button>
                <button>Appearance</button>
                <button>App</button>
            </div>

            <div className="settings_container">
                <div>
                    <img className=""/>
                    <h3>UserName</h3>
                    <p>Role</p>
                </div>
            </div>
        </div>
    )
}

export default Settings;