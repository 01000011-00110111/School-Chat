// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React from "react";
import {Tabs, Tab } from "../static/js/react_tabs";

const Settings = () => {
    return (
        <div className="settings_page">
            <div className="settings_navigation_container">
                <h3>Settings</h3>

                <button>My Profile</button>
                <button>Account</button>
                <button>Notifications</button>
                <button>Appearance</button>
                <button>App</button>
            </div>

            <div className="settings_container">
                <Tabs>
                    <Tab label={"Account"}>
                        <img className=""/>
                        <h3>UserName</h3>
                        <p>Role</p>
                    </Tab>

                    <Tab label={"p"}>
                        p
                    </Tab>
                </Tabs>
            </div>
        </div>
    )
}

export default Settings;