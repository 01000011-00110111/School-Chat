// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React from 'react'
import { useState, useEffect } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus, faPaperPlane, faBars, faBorderAll, faGear, faRightFromBracket } from '@fortawesome/free-solid-svg-icons'
// import { io } from "socket.io-client";
import socket from '../socket'

// const socket = io("http://127.0.0.1:8000");

function Chat() {
    const [chatrooms, setChatooms] = useState([])
    const [users, setUsers] = useState([{}])
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    useEffect(() => {
        socket.on("server_message", (data) => {
            setMessages((prev) => [...prev, data.message]);
        });

        return () => {
            socket.off("server_message");
        };
    }, []);
    
    const sendMessage = (e) => {
        if ((e?.key === 'Enter' || e === undefined) && input.trim() !== '') {
            socket.emit("client_message", { message: input });
            setInput("");
        }
    };

    document.addEventListener('keydown', sendMessage);
  
    function changeChatRoom(room_name) {
      
      window.history.pushState({ room_name }, '', `/chat/${room_name}`)
      updateChatRoom(room_name);
    }
  
    function updateChatRoom(room_name) {
      const room_display = document.getElementById("room_display");
      room_display.innerHTML = room_name;
    }
  
    document.addEventListener('DOMContentLoaded', () => {
      const currentRoom = window.location.pathname.split('/')[2] || 'Main';
      updateChatRoom(currentRoom);
    })
  
    const open_sidenav = () => {
      const sidenav = document.getElementsByClassName("sidenav")[0];
      if (!sidenav.classList.contains('sidenav_opened')) {
        sidenav.classList.add("sidenav_opened");
      }
      else {
        sidenav.classList.remove("sidenav_opened");
      }
    }
  
    return (
    <div className='main'>
        <div className='sidenav'>
            <div className='sidenav_dropdown'>
                <div className='sidenav_button'>
                <FontAwesomeIcon icon={faBorderAll}/>
                <p>Chat Rooms</p>
                </div>
                <ul className='sidenav_dropdown content'>

                </ul>
            </div>
  
            <a href='/settings' className='sidenav_button'>
            <FontAwesomeIcon icon={faGear}/>
            <p>Settings</p>
            </a>
            <a href='/logout' className='sidenav_button'>
            <FontAwesomeIcon icon={faRightFromBracket}/>
            <p>Logout</p>
            </a>
        </div>
  
        <div className='chat_container'>
            <div className='topbar'>
            <div>
                <button onClick={() => open_sidenav()} id='nav_button'>
                <FontAwesomeIcon icon={faBars}/>
                </button>
                <h2 id='room_display'></h2>
            </div>
            <img alt='A users profile' src='/react-sanic-app/src/logo.svg' className='profile_button'/>
            </div>
            
            <div className='main_chat_body'>
            <div className='chat'>
                {messages.map((msg, idx) => (
                    <div key={idx} className="user_message">
                        <div className='message_image_container'>
                            <img src='/static/images/AppIcon.png' alt='a users picture' className='user_profile_pciture'/>
                        </div>
                        <div className="message_info">
                            <div className="message_info_container">
                                <p>User</p>
                                <p>*</p>
                                <p>Fri Dec 06 01:44 PM</p>
                            </div>

                            <div className="message_content_container">
                                {msg}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
  
            <div className='user_list'>
                <input type='text' placeholder='Search for a user' id='user_search_input'/>
            </div>
            </div>
  
            <div className='bottom_bar'>
            <div className='message_box'>
            <input id='file_import_input' type='file' title='files'/>
            <label htmlFor="file_import_input" id='file_import_button'>
                <FontAwesomeIcon icon={faPlus} />
            </label>
                <input type='text' 
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder='Type your message' 
                    id='message_input' 
                    autoCapitalize='true' 
                    autoCorrect='true' 
                    spellCheck='true'/>
                <button 
                    id='send_button' 
                    onClick={sendMessage}>
                <FontAwesomeIcon icon={faPaperPlane}/>
                </button>
            </div>
            </div>
        </div>
    </div>
    )
}
  
export default Chat