// Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React, { useState } from "react";
import { Prompt, PromptStep, EmailBox, TextBox, LineColorDialog, WebEmbed, CheckBox } from "../static/js/native";
import socket from "../socket";

function Signup() {
    const [formInfo, setformInfo] = useState({
        displayName: "",
        role: "",
        usernameColor: "#ffffff",
        roleColor: "#ffffff",
        messageColor: '#000000',
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        conditionsAccepted: false,
    });

    const setInformation = (event) => {
        const {name, value} = event.target;        
        setformInfo(prevState => ({
            ...prevState,
            [name]: value,
        }));

        console.log(value)
    };

    const sendDataToServer = () => {
        socket.emit('signup', {
            email: formInfo.email,
            username: formInfo.username,
            displayName: formInfo.displayName,
            password: formInfo.password,
            confirmPassword: formInfo.confirmPassword,
            role: formInfo.role,
            displayNameColor: formInfo.usernameColor,
            roleColor: formInfo.roleColor,
            messageColor: formInfo.messageColor,
            userColor: formInfo.usernameColor,
            agreeToTerms: formInfo.conditionsAccepted === "on" ? true : false
        });
    }

    return (
        <div className="signup-main">
            <Prompt>
                <PromptStep title={"Creation"}>   
                    <EmailBox label={"Email"} placeholder={"Enter an email address"} onUpdate={setInformation} default_value={formInfo.email} name="email"/>
                    <TextBox label={"Username"} placeholder={"Provide a username"} onUpdate={setInformation} default_value={formInfo.username} name="username"/>
                    <TextBox label={"Display Name"} placeholder={"Provide a displayname"} onUpdate={setInformation} default_value={formInfo.displayName} name="displayName"/>
                    <TextBox label={"Password"} placeholder={"Provide a password"} hidden onUpdate={setInformation} default_value={formInfo.password} name="password"/>
                    <TextBox label={"Confirm Password"} placeholder={"Please confirm the previous entered password"} hidden onUpdate={setInformation} default_value={formInfo.confirmPassword} name="confirmPassword"/>
                </PromptStep>

                <PromptStep title={"Customization"}>
                    <TextBox label={"Role"} placeholder={"Enter a custom role"} onUpdate={setInformation} default_value={formInfo.role} name="role"/>

                    <div className="dialog-content">
                        <LineColorDialog title="Display Name Color" onChange={setInformation} default_value={formInfo.usernameColor} name="usernameColor"/>
                        <LineColorDialog title="Role Color" onChange={setInformation} default_value={formInfo.roleColor} name="roleColor"/>
                        <LineColorDialog title="Message Color" onChange={setInformation} default_value={formInfo.messageColor} name="messageColor"/>
                    </div>
                </PromptStep>

                <PromptStep title={"Agreements"}>
                    <WebEmbed url={"./TERMS OF SERVICE.pdf#toolbar=0&navpanes=0&scrollbar=0"} title={"Terms & Conditions"}/>
                    <CheckBox label={"Agree to Terms & Conditions"} onUpdate={setInformation} checked={formInfo.conditionsAccepted} name="conditionsAccepted"/>
                </PromptStep>

                <PromptStep title={"Finalization"}>
                    <h1>Congratulations you're finished Signing up!</h1>
                    <button onClick={sendDataToServer}>Submit</button>
                </PromptStep>
            </Prompt>
        </div>
  );
}

export default Signup;