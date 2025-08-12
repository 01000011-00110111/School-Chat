/* eslint-disable jsx-a11y/anchor-is-valid */
import React, {useState} from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUpRightFromSquare, faChevronLeft, faDownload, faUserCircle } from "@fortawesome/free-solid-svg-icons";

const ToggleButton = ( {onToggle = function(){}} ) => {
    const [isToggled, setIsToggled] = useState(false);
    const switch_label = document.querySelectorAll(".switch");
    
    
    function tryToggle() {
        const input = document.querySelectorAll('input');

        for (let index = 0; index < input.length; index++) {
            if (input[index].checked === true) {
                setIsToggled(true);    

                
            } else {
                setIsToggled(false);
            }
            
            if (!isToggled) {
                return onToggle()
            }
        }

        
    }

    return (
        <label className="switch">
            <input type="checkbox" onChange={() => tryToggle()}/>
            <span className="slider"></span>
        </label>
    );
}

const TextBox = ({label, placeholder, default_value, hidden, hidden_char, onUpdate, name}) => {
    return (
        <fieldset className="textbox">
            <legend>{label}</legend>
            <input type={hidden ? "password" : "text"} placeholder={placeholder} value={null ? null : default_value} onInput={onUpdate} name={name}/>
        </fieldset>
    )
}

const EmailBox = ({label, placeholder, default_value, onUpdate, name}) => {
    return (
        <fieldset className="textbox">
            <legend>{label}</legend>
            <input type="email" placeholder={placeholder} value={null ? null : default_value} onInput={onUpdate} name={name}/>
        </fieldset>
    )
}

const CheckBox = ({ label, checked, disabled, onUpdate, name, value, onInput }) => {
    return (
        <label className="native_checkbox">
            <input type="checkbox" className="check_input" checked={checked} disabled={disabled} onChange={onUpdate} name={name} value={value} onInput={onInput} />
            <span className="checkmark"></span>
            {label}
        </label>
    )
}

const Card = ({ width, height, children, label }) => {
    return (
        <div className="Card" style={{width: width, height: height}}>
            <p>{label}</p>
            {children}
        </div>
    )
}

function FooterAlert({message, buttons = [], func = []}) {
    return (
        <div className="footer_alert">
            <div className="left_container">
                <p>{message}</p>
            </div>
            <div className="right_container">
                {buttons.map((button, index) => {
                    return (
                        <button key={index} onClick={func[index]}>{buttons[index]}</button>
                    )
                })}
            </div>
        </div>
    )
}

const Modal = ({children}) => {
    return (
        <div className="modal">
            {children}
        </div>
    )
}

function LineButton({children}) {
    return (
        <div className="line_button">
            {children}
        </div>
    )
}

function ColoredBar({colors = []}) {
    return (
        <div style={{backgroundImage:
            `
            linear-gradient(to right, ${
                colors.map((color, index) => (
                    colors[index]
                ))
            })
            `
        }} className="colored_bar"></div>
    )
}

function LineColorDialog({title = "", id = "", className = "", onUpdate, onChange, default_value, name}) {
    return (
        <label className="color_dialog" htmlFor={id}>
            <input type="color" id={id} className={className} onInput={onUpdate} value={null ? null : default_value} onChange={onChange} name={name}/>
            <p>{title}</p>
        </label>
    )
}

function Prompt({children}) {
    const [step, currentStep] = useState(0);
    
    return (
        <div className="signup-prompt">
            <div className="signup-bar">
                <a onClick={() => step === 0 ? window.location.href = '/' : currentStep(step-1)} title={step === 0 ? "Return to login screen" : "Return to previous step"}>
                <FontAwesomeIcon icon={faChevronLeft}/>
                {step === 0 ? "Cancel" : "Back"}
                </a>

                <h3>{children[step]["props"]["title"]}</h3>

                <FontAwesomeIcon icon={faUserCircle} fontSize={27}/>
            </div>

            {children[step]}

            <div>
                <span className="step-count">
                    <p>Step: {step+1}/{children.length}</p>

                    <div className="step-container">
                        {children.map((num, key) => (
                            <span className="progressbar" style={step === key ? {background: "#29c3ff"} : {background: ""}} key={key} onClick={() => currentStep(key)}></span>
                        ))}
                    </div>

                    <button className="navigate-button" onClick={() => step+1 === children.length ? currentStep(0) : currentStep(step+1)}>
                        {step+1 === children.length ? "Finish" : "Continue"}
                    </button>
                </span>
            </div>

        </div>
    )
}

function StepTitle() {
    return (
        <h3>{}</h3>
    )
}

function PromptStep({children, title}) {
    return (
        <span className="prompt-step">
            {children}
        </span>
    )
}

function WebEmbed({ url, title, options = {} }) {
    return (
        <div className="native-web-embed">
            <iframe title={title} src={url}/>
            <div className="native-web-embed-controls">
                <div className="button-container">
                    <a href={url} target="_blank" rel="noreferrer">
                        <FontAwesomeIcon icon={faArrowUpRightFromSquare}/>
                    </a>

                    <a href={url} download={"TERMS AND CONDITIONS.pdf"}>
                        <FontAwesomeIcon icon={faDownload }/>
                    </a>
                </div>
                <p>{title}</p>
            </div>
        </div>
    )
}

const Poll = ({ title="", max, value=0, poll_options = {} }) => {
    const [pollStats, setPollStats] = useState(poll_options);
    console.log(pollStats)

    return (
        <div className="poll">
            <p className="poll-title">{title}</p>
            <div className="poll-options-container">
                {Object.entries(pollStats).map((acc, key, index) => (
                    <div className="poll-options-parent">
                        <div className="poll-option">
                            <p className="poll-option-text">{acc[0]}</p>
                            <div className="poll-option-fill" style={{width: `${pollStats[acc[0]]}%`}}></div>
                        </div>
                        <p>{pollStats[acc[0]]}%</p>
                        {console.log(pollStats["button 1"] )}
                    </div>
                ))}
            </div>
        </div>
    )
}

export {ToggleButton, TextBox, EmailBox, CheckBox, Card, FooterAlert, Modal, LineButton, ColoredBar, LineColorDialog, Prompt, PromptStep, StepTitle, WebEmbed, Poll}