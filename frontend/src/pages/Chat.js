// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus, faPaperPlane, faBorderAll, faGear, faRightFromBracket, faMessage, faChevronRight, faXmark, faUserPlus } from '@fortawesome/free-solid-svg-icons'
import socket from '../socket'
import { Chat_object, renderMessage, renderChat, loadChat } from '../static/js/message'
import { storage } from '../static/js/storage'
import { UserList } from '../static/js/online'
import { update_appbadge } from "../static/js/app_badge";
import { Theme_System } from "../customization/theme_render";

function Chat() {
    const [chatrooms, setChatooms] = useState([]);
    const [users, setUsers] = useState([{}]);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [rooms, setRooms] = useState([]);

    let suuid = sessionStorage.getItem("suuid");
    let rid = sessionStorage.getItem("roomid");

    useEffect(() => {
        socket.emit("check_suuid", suuid);
        socket.emit("chatpage", { suuid: suuid });
        socket.emit("join_room", { roomid: "ilQvQwgOhm9kNAOrRqbr", suuid: suuid });
    }, [suuid]);

    useEffect(() => {
        socket.on("message", (data) => {
            renderChat(data["message"]);
            setMessages([...messages, data["message"]]);
        });

        return () => {
            socket.off("message");
        };
    }, [messages]);

    useEffect(() => {
        socket.on("reset_chat", (msg) => {
            let chatDiv = document.getElementById("chat");
            chatDiv.innerHTML = "";
            renderChat(msg);
        });

        return () => {
            socket.off("reset_chat");
        };
    }, []);

    useEffect(() => {
        socket.on("load_chat", (data) => {
            console.log(data['messages'])
            updateChatRoom(data["roomid"], data["name"]);
            sessionStorage.setItem("roomid", data["roomid"]);
            loadChat(data["messages"]);
            setMessages(data["messages"]);
        });

        return () => {
            socket.off("load_chat");
        };
    }, []);

    const storeText = (event) => {
        const {value} = event.target;
        setInput(value);
        get_remaining_chars();
    };

    function get_remaining_chars() {
        const message = document.getElementById("message_input");
        const remaining_chars_display = document.getElementById("remaining_chars");

        // Retrieve the HTML element's attributes required
        let max_length = message.getAttribute("maxlength");
        let message_length = input.length;
        let total_remaining_chars = max_length - message_length;

        // Checks to see if the total messsage length is greater than 100 if so then change the text color to default (white)
        if (total_remaining_chars > 100) {
            remaining_chars_display.style.color = "white";
        }
        
        // Checks to see if the total messsage length is less than or equal to 100 but more than 20 if so then change the text color to yellow
        else if (total_remaining_chars <= 100 && total_remaining_chars > 20) {
            remaining_chars_display.style.color = "yellow";
        }

        // Checks to see if the total messsage length is less than or equal to 20 if so then change the text color to red
        else if (total_remaining_chars <= 20) {
            remaining_chars_display.style.color = "red";
        };

        // Sets the remaining text to the total amount of characters left
        remaining_chars_display.innerHTML = `${total_remaining_chars} Characters Left`;
        return total_remaining_chars;
    };

    useEffect(() => {
        get_remaining_chars();
    });

    const sendMessage = (e) => {
        if (input.trim() !== "") {
            e?.preventDefault();
            socket.emit("message", { message: input, roomid: rid, suuid: suuid });
            setInput("");
            update_appbadge();
        }
    };

    const logout = () => {
        socket.emit("logout", { suuid: suuid });
    };

    function changeChatRoom(roomid, roomName) {
        if (roomid !== rid) {
            window.history.pushState({ roomName }, "", `/chat/${roomName}`);
            updateChatRoom(roomid, roomName);
            socket.emit("join_room", { roomid: roomid, suuid: suuid });

            if (
                JSON.parse(storage.get("app-nav-settings"))["nav_close_onroom"] === true
            ) {
                open_sidenav();
            }
        }
    }

    useEffect(() => {
        socket.on("room_list", (data) => {
            setRooms(data["rooms"]);
            setChatooms(data["rooms"]);
        });

        return () => {
            socket.off("room_list");
        };
    }, []);

    useEffect(() => {
        socket.on("send_to_login", (data) => {
            suuid = '';
            sessionStorage.removeItem("suuid");
            window.location.href = "/";
        });

        return () => {
            socket.off("send_to_login");
        };
    }, []);

    function updateChatRoom(roomid, room_name) {
        const room_display = document.getElementById("room_display");
        rid = roomid;
        room_display.innerHTML = "/" + room_name;
    }

    window.addEventListener("popstate", (event) => {
        const roomName = event.state ? event.state.roomName : "Main";
        updateChatRoom(rid, roomName);
    });

    document.addEventListener("DOMContentLoaded", () => {
        const currentRoom = window.location.pathname.split("/")[2] || "Main";
        updateChatRoom(rid, currentRoom);
          socket.emit("join_room", { roomid: 'ilQvQwgOhm9kNAOrRqbr', suuid: suuid });
    });

    const open_sidenav = () => {
        const sidenav = document.getElementsByClassName("sidenav")[0];
        if (!sidenav.classList.contains("sidenav_opened")) {
            sidenav.classList.add("sidenav_opened");
        } else {
            sidenav.classList.remove("sidenav_opened");
        }
    };

    const tms = new Theme_System();
    tms.set_theme([
        "linear-gradient(90deg,#9A93D8 13%, #007B79 58%, #384E82 91%)",
        "#19191949",
        "#19191949",
        "white",
        "#ffffff", // This is the usercard, it doesn't work?
        "#19191949",
        "white",
        "purple",
        "white",
        "transparent",
        "white",
        "white", // Doesn't work
        "rgb(0, 94, 255)",
        "white",
        "#19191949",
        "white",
    ]);
    tms.render();

    return (
        <div className="main">
            <div className="topbar">
                <div>
                    <h2 id="room_display" onClick={() => open_sidenav()}>
                        loading...
                    </h2>
                </div>
            </div>

            <div className="chat_container">
                <div className="sidenav">
                    <div className="sidenav_dropdown">
                        <div className="sidenav_button">
                            <FontAwesomeIcon icon={faBorderAll} />
                            <p>Chat Rooms</p>
                        </div>
                        <ul className="sidenav_dropdown content" id="room_list">
                            {rooms.map(([name, value], index) => (
                                <li key={index} onClick={() => changeChatRoom(value, name)}>
                                    {name}
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="nav_buttons_container">
                        <a href='.' className='sidenav_button'>
                            <p>DMs</p>
                        </a>

                        <a href='.' className='sidenav_button'>
                            <p>Create Chat</p>
                        </a>

                        <a href='/settings' className='sidenav_button'>
                            <FontAwesomeIcon icon={faGear}/>
                            <p>Settings</p>
                        </a>
                        
                        <a className='sidenav_button' onClick={logout}>
                            <FontAwesomeIcon icon={faRightFromBracket} color='red'/>
                            <p>Logout</p>
                        </a>
                    </div>

                    <div className="profile_card">
                        <img
                            className="profile_button"
                            alt="profile"
                            src="/icons/favicon.ico"
                        />
                        <div className="profile_user_preview">
                            <p id="profile_card_username">User #1</p>
                            <div className="profile_status">
                                <div id="profile_status_indicator"></div>
                                <p>Online</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="chat_center">
                    <div className="chat" id="chat"></div>

                    <div className="bottom_bar">
                        <label htmlFor="file_import_input" id="file_import_button">
                            <FontAwesomeIcon icon={faPlus} />
                            <input id="file_import_input" type="file" title="files" />
                        </label>

                        <p id="remaining_chars">250 Characters Left</p>

                        <div className="message_box">
                            <input
                                type="text"
                                value={input}
                                onChange={storeText}
                                placeholder="Type your message"
                                maxLength={250}
                                id="message_input"
                                autoCapitalize="true"
                                autoCorrect="true"
                                spellCheck="true"
                                onKeyDown={(e) => {
                                    if (e.key === "Enter") {
                                        sendMessage();
                                    }
                                }}
                            />
                        </div>

                        <button id="send_button" onClick={sendMessage}>
                            <FontAwesomeIcon icon={faPaperPlane} />
                        </button>
                    </div>
                </div>
                
                <UserList />
            </div>

            <div className="background_blur">
                <div className="user_profile_modal">
                    <div className="profile_modal_options">
                        <div className="profile_modal_button">
                            <span>
                                <FontAwesomeIcon icon={faUserPlus} />
                                <p>Add Friend</p>
                            </span>
                            <FontAwesomeIcon icon={faChevronRight} />
                        </div>

                        <div className="profile_modal_button">
                            <span>
                                <FontAwesomeIcon icon={faMessage} />
                                <p>DM</p>
                            </span>
                            <FontAwesomeIcon icon={faChevronRight} />
                        </div>
                    </div>

                    <div className="profile_details">
                        <button className="close_modal_button">
                            <FontAwesomeIcon icon={faXmark} />
                        </button>
                        <div className="modal_user_details">
                            <img src={null} id="modal_user_picture" alt="something!"/>
                            <div className="modal_extra_details">
                                <h1 id="modal_user_name">Display Name</h1>
                                <p id="modal_user_role">Role</p>
                            </div>
                        </div>
                        <div className="modal_badge_list">
                            <p className=" badge admin">admin</p>
                            <p className="badge mod">OG Badge</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Chat;
