import React, { useState } from "react";
import socket from "../socket";

function Signup() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("");
  const [userColor, setUserColor] = useState("#ffffff");
  const [roleColor, setRoleColor] = useState("#ffffff");
  const [messageColor, setMessageColor] = useState("#ffffff");
  const [agreeToTerms, setAgreeToTerms] = useState(false);

  const sendDataToServer = () => {
    console.log({
      email,
      username,
      displayName,
      password,
      confirmPassword,
      role,
      userColor,
      roleColor,
      messageColor,
      agreeToTerms,
    });
    socket.emit("signup", {
      email,
      username,
      displayName,
      password,
      confirmPassword,
      role,
      userColor,
      roleColor,
      messageColor,
      agreeToTerms,
    });
  };

  return (
    <div className="signup-main">
      <h1>Signup</h1>
      <section>
        <h2>Creation</h2>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            placeholder="Enter an email address"
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            placeholder="Provide a username"
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Display Name:</label>
          <input
            type="text"
            value={displayName}
            placeholder="Provide a display name"
            onChange={(e) => setDisplayName(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            placeholder="Provide a password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <label>Confirm Password:</label>
          <input
            type="password"
            value={confirmPassword}
            placeholder="Confirm your password"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
      </section>
      <section>
        <h2>Customization</h2>
        <div>
          <label>Role:</label>
          <input
            type="text"
            value={role}
            placeholder="Enter a custom role"
            onChange={(e) => setRole(e.target.value)}
          />
        </div>
        <div>
          <label>Display Name Color:</label>
          <input
            type="color"
            value={userColor}
            onChange={(e) => setUserColor(e.target.value)}
          />
        </div>
        <div>
          <label>Role Color:</label>
          <input
            type="color"
            value={roleColor}
            onChange={(e) => setRoleColor(e.target.value)}
          />
        </div>
        <div>
          <label>Message Color:</label>
          <input
            type="color"
            value={messageColor}
            onChange={(e) => setMessageColor(e.target.value)}
          />
        </div>
      </section>
      <section>
        <h2>Agreements</h2>
        <div>
          <a
            href="./TERMS OF SERVICE.pdf#toolbar=0&navpanes=0&scrollbar=0"
            target="_blank"
            rel="noopener noreferrer"
          >
            Terms &amp; Conditions
          </a>
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              checked={agreeToTerms}
              onChange={(e) => setAgreeToTerms(e.target.checked)}
            />
            Agree to Terms &amp; Conditions
          </label>
        </div>
      </section>
      <section>
        <h2>Finalization</h2>
        <p>Congratulations, you're finished signing up!</p>
        <button onClick={sendDataToServer}>Send data to server</button>
      </section>
    </div>
  );
}

export default Signup;