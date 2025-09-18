// Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, {useState} from "react";

function set_tab() {}

function Tabs({ children }) {
    const [activeTab, setActiveTab] = useState(0);
    set_tab = (tab_index) => {setActiveTab(tab_index)}
    return (
      <div>
        {children[activeTab]}
      </div>
    );
}
  
function Tab({ label, children, style={} }) {
    return (
      <div style={style}>
        {children}
      </div>
    );
}

function TabButton({ label, tab_index, icon}) {
    return (
      <button onClick={() => set_tab(tab_index)}>
        <FontAwesomeIcon icon={icon}/>
        {label}
      </button>
    );
}

export {Tabs, Tab, TabButton}