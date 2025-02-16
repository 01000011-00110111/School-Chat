import React, {useState, useEffect} from "react";
import { CheckBox, EmailBox, LineColorDialog, Prompt, PromptStep, TextBox, WebEmbed } from "../static/js/native";
import socket from '../socket'

function Signup() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [displayName, setDisplayName] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [role, setRole] = useState("");
    const [displayNameColor, setDisplayNameColor] = useState("#000000");
    const [roleColor, setRoleColor] = useState("#000000");
    const [messageColor, setMessageColor] = useState("#000000");
    const [agreeToTerms, setAgreeToTerms] = useState(false);

    const sendDataToServer = () => {
        socket.emit('signup', {
            email,
            username,
            displayName,
            password,
            confirmPassword,
            role,
            displayNameColor,
            roleColor,
            messageColor,
            agreeToTerms
        });
    }

    return (
        <div className="signup-main">
            <Prompt>
                <PromptStep title={"Creation"}>   
                    <EmailBox label={"Email"} placeholder={"Enter an email address"} onChange={(e) => setEmail(e.target.value)}/>
                    <TextBox label={"Username"} placeholder={"Provide a username"} onChange={(e) => setUsername(e.target.value)}/>
                    <TextBox label={"Display Name"} placeholder={"Provide a displayname"} onChange={(e) => setDisplayName(e.target.value)}/>
                    <TextBox label={"Password"} placeholder={"Provide a password"} hidden onChange={(e) => setPassword(e.target.value)}/>
                    <TextBox label={"Confirm Password"} placeholder={"Please confirm the previous entered password"} hidden onChange={(e) => setConfirmPassword(e.target.value)}/>
                </PromptStep>

                <PromptStep title={"Customization"}>
                    <TextBox label={"Role"} placeholder={"Enter a custom role"} onChange={(e) => setRole(e.target.value)}/>

                    <div className="dialog-content">
                        <LineColorDialog title="Display Name Color" onChange={(color) => setDisplayNameColor(color)}/>
                        <LineColorDialog title="Role Color" onChange={(color) => setRoleColor(color)}/>
                        <LineColorDialog title="Message Color" onChange={(color) => setMessageColor(color)}/>
                    </div>
                </PromptStep>

                <PromptStep title={"Agreements"}>
                    <WebEmbed url={"./TERMS OF SERVICE.pdf#toolbar=0&navpanes=0&scrollbar=0"} title={"Terms & Conditions"}/>
                    <CheckBox label={"Agree to Terms & Conditions"} onChange={(e) => setAgreeToTerms(e.target.checked)}/>
                </PromptStep>

                <PromptStep title={"Finalization"}>
                    <h1>Congratulations you're finished Signing up!</h1>
                    <button onClick={sendDataToServer}>Send data to server</button>
                </PromptStep>
            </Prompt>
        </div>
    )
}

export default Signup
