// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub } from "@fortawesome/free-brands-svg-icons";
import {Tabs, Tab, TabButton } from "../static/js/react_tabs";
import { ToggleButton, TextBox, CheckBox, Card, FooterAlert, Modal, LineButton, ColoredBar, LineColorDialog, EmailBox } from "../static/js/native";
import { storage } from "../static/js/storage";
import { faArrowLeft, faAsterisk, faBell, faCircle, faHomeUser, faLaptopFile, faUserAlt } from "@fortawesome/free-solid-svg-icons";

const Settings = () => {
    const getInitialState = () => {
        const value = JSON.parse(storage.get("app-nav-settings"))["nav_close_onroom"];
        return value;
    }

    const [navState, setNavState] = useState(getInitialState);

    const handleChange = (event) => {
        setNavState(event.target.value);
        storage.set("app-nav-settings", `{"nav_close_onroom": ${event.target.value}}`)
    }

    const activate_notifications = () => {
        if (!"Notification" in window) {
            alert("This browser does not support desktop notifications");
        } 
        
        else if (Notification.permission === "granted") {
            const notification = new Notification("Notifications have been activated!");
        }

        else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    const notification = new Notification("Notifications have been activated!");
                }
            });
        }
    }

    return (
        <div className="settings_page">
            <div className="settings_navigation_container">
                <div className="settings_control_header">
                    <button onClick={() => window.location.href = "./chat/Main"} className="return_button">
                        <FontAwesomeIcon icon={faArrowLeft}/>
                    </button>
                    <h3>Settings</h3>
                </div>
                <TabButton label={"My Profile"} icon={faUserAlt} tab_index={0}/>
                <TabButton label={"Account"} icon={faHomeUser} tab_index={1}/>
                <TabButton label={"Notifications"} icon={faBell} tab_index={2}/>
                <TabButton label={"Preferences"} icon={faAsterisk} tab_index={3}/>
                <TabButton label={"App"} icon={faLaptopFile} tab_index={4}/>
            </div>

            <div className="settings_container">
                <Tabs>
                    <Tab label={"My Profile"} style={{display: "flex", gap: "2pc", paddingTop: "12px"}}>
                        <label htmlFor="profile" className="profile_picture_container">
                            {/* <div className="hover_container"></div> */}
                        </label>

                        <Card height={"15rem"} width={"200px"} label={"Profile"}>
                            <label htmlFor="profile">
                                <img src={"/icons/favicon.ico"} className="user_picture" draggable="false" alt="The-Dev"/>
                                <input type="file" accept="image/*" id="profile"/>
                            </label>
                            <h3 contentEditable spellCheck="false">The-Dev</h3>
                            
                            <p contentEditable spellCheck="false">Benchy Master</p>
                        </Card>

                        <Card label={"Profile Colors"}>
                            <LineColorDialog title="Username Color" id="username_color"/>
                            <LineColorDialog title="Role Color" id="role_color"/>
                            <LineColorDialog title="Message Color" id="message_color"/>
                        </Card>
                    </Tab>

                    <Tab label={"Account"}>
                        <h2>Account</h2>
                        <p>Change your username</p>
                        <TextBox label={"Username"} placeholder={"Enter Username"}/>

                        <p>Change your email</p>
                        <EmailBox label={"Email"} placeholder={"Enter Email"}/>
                    </Tab>

                    <Tab label={"Notifications"}>
                        <h2>Notifications</h2>
                        <ToggleButton onToggle={() => activate_notifications()}/>
                        <CheckBox label={"New Message"} disabled={false}/>
                        <CheckBox label={"User Ping"} disabled={false}/>
                        <CheckBox label={"Private Message"} disabled={false}/>
                    </Tab>

                    <Tab label={"Appearance"}>
                        <h2>Appearance</h2>
                        <CheckBox label={"Sync theme across devices"}/>
                        <Modal>
                            <LineButton>
                                <div style={{display: "flex", alignItems: "center", gap: "0.4rem"}}>
                                    <p>Dark</p>
                                    <FontAwesomeIcon icon={faCircle} fontSize={"7px"}/>
                                    <p>System</p>
                                </div>
                                <ColoredBar colors={["black", "gray", "lightgrey"]}/>
                            </LineButton>

                            <select>
                                <option>Dark</option>
                                <option>Light</option>
                                <option>Better Dark</option>
                            </select>
                        </Modal>

                        <h2>Chat</h2>

                        <p>Close side navigational bar on chat room selection</p>
                        <select value={navState} onChange={handleChange}>
                            <option value={false}>No</option>
                            <option value={true}>Yes</option>
                        </select>
                    </Tab>

                    <Tab label={"App"}>
                        <a href="https://github.com/01000011-00110111/School-Chat" style={{alignItems: "center", display: "flex", height: "fit-content", gap: "0.4rem", margin: "3rem 0"}}>
                        <FontAwesomeIcon icon={faGithub} fontSize={50}/>
                        Source Code
                        </a>
                    </Tab>
                </Tabs>
                <FooterAlert message={"You have unsaved changes"} buttons={["Discard", "Save"]} func={[() => console.log("Button1"), () => console.log("Button2")]}/>
            </div>
        </div>
    )
}

export default Settings;