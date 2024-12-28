import React, {useState} from "react";

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

const TextBox = ({label, placeholder, default_value}) => {
    return (
        <fieldset className="textbox">
            <legend>{label}</legend>
            <input type="text" placeholder={placeholder} value={null ? null : default_value}/>
        </fieldset>
    )
}

const CheckBox = ({ label, checked, disabled }) => {
    return (
        <label className="native_checkbox">
            <input type="checkbox" className="check_input" checked={checked} disabled={disabled}/>
            <span className="checkmark"></span>
            {label}
        </label>
    )
}

const Card = ({ width, height, children }) => {
    return (
        <div className="Card" style={{width: width, height: height}}>
            <p>Profile</p>
            {children}
        </div>
    )
}

function FooterAlert({message, color, buttons = [], func = []}) {
    return (
        <div className="footer_alert" style={document.querySelector(":root").style.setProperty("--alert_color", color)}>
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

export {ToggleButton, TextBox, CheckBox, Card, FooterAlert, Modal, LineButton, ColoredBar}