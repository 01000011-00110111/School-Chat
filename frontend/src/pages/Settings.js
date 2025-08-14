// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub } from "@fortawesome/free-brands-svg-icons";
import {Tabs, Tab, TabButton } from "../static/js/react_tabs";
import { ToggleButton, TextBox, CheckBox, Card, FooterAlert, Modal, LineButton, ColoredBar, LineColorDialog, EmailBox } from "../static/js/native";
import { storage } from "../static/js/storage";
import { faArrowLeft, faAsterisk, faBell, faCircle, faHomeUser, faLaptopFile, faUserAlt } from "@fortawesome/free-solid-svg-icons";
import socket from "../socket";

const Settings = () => {
    const [errors, SetErrors] = useState([]);
    
    const getInitialState = () => {
        if (!storage.get("app-nav-settings")) {
            storage.set("app-nav-settings", '{"nav_close_onroom": false}');
        }

        const value = JSON.parse(storage.get("app-nav-settings"))["nav_close_onroom"];
        return value;
    }
    let suuid = sessionStorage.getItem("suuid");

    useEffect(() => {
        socket.emit("check_suuid", suuid);
    });

    useEffect(() => {
        socket.on("send_to_login", (data) => {
            suuid = '';
            sessionStorage.removeItem("suuid");
            window.location.href = "/";
        });

        return () => {
            socket.off("send_to_login");
        };
    }, []);

    const on_update = (event = Event) => {
        // console.log("Changes detected!")
        document.querySelectorAll(".footer_alert")[0].classList.add("on_screen");
    }

    useEffect(() => {
        socket.emit("get_settings", window.sessionStorage.getItem("suuid"));
    }, [])
    
    
    const [navState, setNavState] = useState(getInitialState);
    const [formInfo, setformInfo] = useState({
        displayName: "",
        role: "",
        usernameColor: "#000000",
        roleColor: "#000000",
        messageColor: "#000000",
        username: "TestAcc",
        email: "testemail@123.com",
        newMessagePing: false,
        userPing: true,
        privateMessagePing: false,
    });
    
    useEffect(() => {
        socket.on("settings", (data) => {
            if (data.status === "error") {
                const error_array = [];
                Object.entries(data["errors"]).map((error, index) => {
                    error_array.push(error[1][1])
                })
                SetErrors(error_array);
            } else {
                SetErrors([]);
                document.querySelectorAll(".footer_alert")[0].classList.remove("on_screen");
            }

            if (data.settings) {
                setformInfo({
                    displayName: data["settings"]["displayName"],
                    role: data["settings"]["role"],
                    usernameColor: data["settings"]["usernameColor"],
                    roleColor: data["settings"]["roleColor"],
                    messageColor: data["settings"]["messageColor"]
                })
            }

        });
    }, [formInfo])

    // console.log(errors)

    const save_settings = () => {
        socket.emit("save_settings", {suuid: window.sessionStorage.getItem("suuid"), formInfo});

    }

    const handleChange = (event) => {
        setNavState(event.target.value);
        storage.set("app-nav-settings", `{"nav_close_onroom": ${event.target.value}}`)
        on_update(event);
    }

    const setInformation = (event) => {
        const {name, value} = event.target;
        setformInfo(prevState => ({
            ...prevState,
            [name]: value,
        }));
        console.log(value)
        console.log(formInfo.newMessagePing)
        on_update(event);
    };

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
                                <input type="file" accept="image/*" id="profile" onChange={(e) => on_update(e)}/>
                            </label>
                            <input spellCheck="false" type="text" value={formInfo.displayName} onChange={setInformation} name="displayName" id="displayname_input" placeholder="Enter Display Name"/>
                            
                            <input spellCheck="false" type="text" value={formInfo.role} onChange={setInformation} name="role" id="role_input" placeholder="Enter Role"/>
                        </Card>

                        <Card label={"Profile Colors"}>
                            <LineColorDialog title="Username Color" id="username_color" onUpdate={setInformation} name="usernameColor" default_value={formInfo.usernameColor}/>
                            <LineColorDialog title="Role Color" id="role_color" onUpdate={setInformation} name="roleColor" default_value={formInfo.roleColor}/>
                            <LineColorDialog title="Message Color" id="message_color" onUpdate={setInformation} name="messageColor" default_value={formInfo.messageColor}/>
                        </Card>
                    </Tab>

                    <Tab label={"Account"}>
                        <h2>Account</h2>
                        <p>Change your username</p>
                        <TextBox label={"Username"} placeholder={"Enter Username"} default_value={formInfo.username} onUpdate={setInformation} name="username"/>

                        <p>Change your email</p>
                        <EmailBox label={"Email"} placeholder={"Enter Email"} default_value={formInfo.email} onUpdate={setInformation} name="email"/>
                    </Tab>

                    <Tab label={"Notifications"}>
                        <h2>Notifications</h2>
                        <ToggleButton onToggle={() => activate_notifications()}/>
                        <CheckBox label={"New Message"} disabled={false} onUpdate={setInformation} name="newMessagePing" checked={formInfo.newMessagePing}/>
                        <CheckBox label={"User Ping"} disabled={false} onUpdate={setInformation} name="userPing" checked={formInfo.userPing}/>
                        <CheckBox label={"Private Message"} disabled={false} onUpdate={setInformation} name="privateMessagePing" checked={formInfo.privateMessagePing}/>
                    </Tab>

                    <Tab label={"Appearance"}>
                        <h2>Appearance</h2>
                        {/* <CheckBox label={"Sync theme across devices"} onUpdate={(e) => on_update(e)}/>
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
                        </Modal> */}

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
                <FooterAlert message={"You have unsaved changes"} buttons={["Discard", "Save"]} func={[() => console.log("Button1"), () => save_settings()]}/>
            </div>
            
            { errors.length === 0 ? "" :
            <div className="settings_edits">
                <h2>Failed to save due to improper settings</h2>
                <ul>
                    {errors.map((error, index) => (
                        <li key={index}>{error}</li>
                    ))}
                </ul>
            </div>}
        </div>
    )
}

export default Settings;