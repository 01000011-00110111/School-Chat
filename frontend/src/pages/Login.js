import React from "react";

function Login() {
    return (
        <div id="login_container">
            <div id="left_login_container">
                <div id="form_header">

                </div>

                <form id="form_container">
                    <div className="wrapper_panel">
                        <div>
                            <p>Username</p>
                        </div>

                        <div className="login_input">
                            <input/>
                        </div>
                    </div>

                    <div className="wrapper_panel">
                        <div>
                            <p>Password</p>
                            <a href="/reset-password">Forgot Password?</a>
                        </div>

                        <div className="login_input">
                            <input/>
                        </div>
                    </div>

                    <div className="wrapper_panel">
                        <button>Login</button>
                    </div>
                </form>

                <div id="links_container">

                </div>
            </div>

            <div id="right_preview_container">
                <h1>School Chat</h1>

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
                            <li>No capitalized words.</li>
                            <li>Keep the language english (unless in a special chat room).</li>
                        </ul>
                    </div>
                    <p>
                        (if you have more rules open the Issue <a href="#">rules</a> and comment the rule there!)
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Login