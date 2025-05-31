import React from "react";
import { Poll } from "../static/js/native";

function Portal() {
    return (
        <div>
            <h1>Portal</h1>
            <Poll title="What feature do you think should be added next?" value={20} poll_options={{
                "button 1": 10,
                "button 2": 20,
                "button 3": 30,
                "button 4": 40,
            }} />
        </div>
    )
}

export default Portal