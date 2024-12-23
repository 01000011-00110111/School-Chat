import React, {useState} from "react";

const ToggleButton = ( {onToggle = function(){}} ) => {
    const [isToggled, setIsToggled] = useState(false);

    if (isToggled) {
        onToggle.call()
    }

    return (
        <div className="toggle-button">
            <input type="checkbox" id="toggle" onChange={() => setIsToggled(true)} />
            <label htmlFor="toggle" className="toggle-label"></label>
        </div>
    );
}

export {ToggleButton}