// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React from "react";
import {Tabs, Tab } from "../static/js/react_tabs";
import { ToggleButton } from "../static/js/native";

const Settings = () => {
    return (
        <div className="settings_page">
            <div className="settings_navigation_container">
                <button>Close</button>
                <button>My Profile</button>
                <button>Account</button>
                <button>Notifications</button>
                <button>Preferences</button>
                <button>App</button>
            </div>

            <div className="settings_container">
                <Tabs>
                    <Tab label={"My Profile"}>
                        <img className="" alt="e"/>
                        <h3>UserName</h3>
                        <p>Role</p>
                    </Tab>

                    <Tab label={"Account"}>
                        <p>Account</p>
                    </Tab>

                    <Tab label={"Notifications"}>
                        <p>Notifications</p>
                        <ToggleButton onToggle={() => new Notification("Hello")}/>
                        <button onClick={() => Notification.requestPermission()}>Grant Notifs</button>
                        <button onClick={() => new Notification("Hello")}>New Notification</button>
                    </Tab>

                    <Tab label={"Appearance"}>
                        <h2>Appearance</h2>

                        <h2>Chat</h2>

                        <p>Close side navigational bar on chat room selection</p>
                        <select>
                            <option>No</option>
                            <option>Yes</option>
                        </select>
                    </Tab>

                    <Tab label={"App"}>
                        <p>App</p>
                    </Tab>
                </Tabs>
            </div>
        </div>
    )
}

export default Settings;