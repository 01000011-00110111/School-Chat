import React, {useState} from "react";

function Tabs({ children }) {
    const [activeTab, setActiveTab] = useState(0);
  
    return (
      <div>
        <ul>
          {children.map((child, index) => (
            <li key={index} onClick={() => setActiveTab(index)}>
              {child.props.label}
            </li>
          ))}
        </ul>
        {children[activeTab]}
      </div>
    );
  }
  
function Tab({ label, children }) {
    return (
      <div>
        {children}
      </div>
    );
}

export {Tabs, Tab}