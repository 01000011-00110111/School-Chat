import React, {useState, useEffect} from "react";
import { CheckBox, EmailBox, LineColorDialog, Prompt, PromptStep, TextBox, WebEmbed } from "../static/js/native";

function Signup() {
    return (
        <div className="signup-main">
            <Prompt>
                <PromptStep title={"Creation"}>   
                    <EmailBox label={"Email"} placeholder={"Enter an email address"}/>
                    <TextBox label={"Username"} placeholder={"Provide a username"}/>
                    <TextBox label={"Display Name"} placeholder={"Provide a displayname"}/>
                    <TextBox label={"Password"} placeholder={"Provide a password"} hidden/>
                    <TextBox label={"Confirm Password"} placeholder={"Please confirm the previous entered password"} hidden/>
                </PromptStep>

                <PromptStep title={"Customization"}>
                    <TextBox label={"Role"} placeholder={"Enter a custom role"}/>

                    <div className="dialog-content">
                        <LineColorDialog title="Display Name Color"/>
                        <LineColorDialog title="Role Color"/>
                        <LineColorDialog title="Message Color"/>
                    </div>
                </PromptStep>

                <PromptStep title={"Agreements"}>
                    <WebEmbed url={"./TERMS OF SERVICE.pdf#toolbar=0&navpanes=0&scrollbar=0"} title={"Terms & Conditions"}/>
                    <CheckBox label={"Agree to Terms & Conditions"}/>
                </PromptStep>

                <PromptStep title={"Finalization"}>
                    <h1>Congratulations you're finished Signing up!</h1>
                </PromptStep>
            </Prompt>
        </div>
    )
}

export default Signup