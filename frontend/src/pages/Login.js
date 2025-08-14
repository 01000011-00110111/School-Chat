import React, {useState, useEffect} from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import socket from '../socket'
import {setSuuid} from '../static/js/variables'

function Login() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [showPassword, setShowPassowrd] = useState({
        passwordState: "password",
        iconState: faEye,
    });
    const [loginStatus, setloginStatus] = useState("");

    useEffect(() => {
        let uuid = sessionStorage.getItem("suuid");
        if (uuid) {
            setSuuid(uuid);
            window.location.href = "/chat/Main";
        }
    }, []);
    
    const show_password = () => {
        showPassword.passwordState !== "text" ? setShowPassowrd({passwordState: "text", iconState: faEyeSlash}) : setShowPassowrd({passwordState: "password", iconState: faEye});
    };

    const handleLogin = (e) => {
        e.preventDefault();
        socket.emit("login", { username: username, password: password });
    };

    socket.on("login", (data) => {
        if (data["status"] === 'successful') {
            setSuuid(data["suuid"]);
            window.location.href = "/chat/Main";
        }
        if (data["status"] === 'failed') {
            // console.log(data);
            setloginStatus("Username or Password is incorrect");
        }
    });


    return (
        <div id="login_container">
            <div id="left_login_container">
                <div id="form_header">
                    <h1>Login</h1>
                    <p>Don't have an account yet? <a href="/signup">Sign Up</a></p>
                </div>

                <div id="form_container">
                    <div className="wrapper_panel">
                        <div className="panel_text">
                            <p>Username</p>
                        </div>

                        <div className="login_input">
                            <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Enter your username" tabIndex={1} required/>
                        </div>
                    </div>

                    <div className="wrapper_panel">
                        <div className="panel_text">
                            <p>Password</p>
                            <a href="/reset-password">Forgot Password?</a>
                        </div>

                        <div className="login_input">
                            <input value={password} onChange={(e) => setPassword(e.target.value)} type={showPassword.passwordState} placeholder="Enter your password" tabIndex={2} required/>
                            <button onClick={() => show_password()}>
                                <FontAwesomeIcon icon={showPassword.iconState}/>
                            </button>
                        </div>
                    </div>

                    <div className="wrapper_panel">
                        <button onClick={handleLogin} className="login_button">Login</button>
                    </div>

                    <p className="login_status">{loginStatus}</p>
                </div>

                <div id="links_container">
                    <a href="https://github.com/01000011-00110111/School-Chat/releases" target="_blank" rel="noreferrer">Releases</a>
                    <a href=".">???</a>
                    <a href="https://github.com/01000011-00110111/School-Chat" target="_blank" rel="noreferrer">Github</a>
                </div>
            </div>

            <div id="right_preview_container">
                <h1 id="Title">School Chat</h1>

                <div className="quick_look_container">
                    <p>School chat was made by cserver, and cseven for chatting with friends but grew into a bigger project.</p>
                    <div className="rules_container">
                        <h2>Rules:</h2>
                        <ul>
                            <li>Do not be racist.</li>
                            <li>No nsfw.</li>
                            <li>Keep cursing to a minimal.</li>
                            <li>Do not make chat room names offensive.</li>
                            <li>Do not spam pings.</li>
                            <li>Keep the language english (unless in a special chat room).</li>
                        </ul>
                    </div>
                    <p style={{color: "red"}}>Breaking the rules will cause you to be muted, continue to break will result in a ban</p>
                    <p>
                        (if you have more rules open the Issue <a href="https://github.com/01000011-00110111/School-Chat/discussions/categories/ideas">rules</a> and comment the rule there!)
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Login

