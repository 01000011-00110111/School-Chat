// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import React, { use } from 'react'
import { useState, useEffect } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus, faPaperPlane, faBars, faBorderAll, faGear, faRightFromBracket, faMessage, faChevronRight, faXmark, faUserPlus } from '@fortawesome/free-solid-svg-icons'
import socket from '../socket'
import { Chat_object, renderMessage, renderChat, loadChat } from '../static/js/message'
import context_menu, { handle_create } from '../static/js/context_menu'
import { storage } from '../static/js/storage'
import { par_user, setupTimer, SetUsersList, ShowModal, user_data } from '../static/js/online'

function Chat() {
    const [chatrooms, setChatooms] = useState([]);
    const [users, setUsers] = useState([{}]);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [rooms, setRooms] = useState([]);
    const [ostatus, setostatus] = useState("")

    useEffect(() => {
        const interval = setInterval(() => {
            setostatus(par_user['data']['status']);
        }, 1000)

        return () => clearInterval(interval)
    })

    let suuid = sessionStorage.getItem("suuid");
    let rid = sessionStorage.getItem("roomid");

    useEffect(() => {
        socket.emit("chatpage", { suuid: suuid });
    }, []);

    useEffect(() => {
        socket.emit("join_room", { roomid: 'ilQvQwgOhm9kNAOrRqbr', suuid: suuid });
    }, []);

    useEffect(() => {
        socket.on("message", (data) => {
            renderChat(data['message']);
            setMessages([...messages, data['message']]);
        });

        return () => {
            socket.off("message");
        };
    }, []);

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
            updateChatRoom(data['roomid'], data['name']);
            sessionStorage.setItem("roomid", data['roomid']);
            loadChat(data['messages']);
            setMessages(data['messages']);
        });

        return () => {
            socket.off("load_chat");
        };
    }, []);
    
    const sendMessage = (e) => {
        if (input.trim() !== '') {
            e?.preventDefault();
            socket.emit("message", { message: input, roomid: rid, suuid: suuid });
            setInput("");
        }
    };

    const logout = () => {
        socket.emit("logout", { suuid: suuid });
    };

    function changeChatRoom(roomid, roomName) {
        if (roomid !== rid) {
            window.history.pushState({ roomName }, '', `/chat/${roomName}`);
            updateChatRoom(roomid, roomName)
            socket.emit("join_room", { roomid: roomid, suuid: suuid });

            if (JSON.parse(storage.get("app-nav-settings"))["nav_close_onroom"] === true) {
                open_sidenav();
            }
        }
    }

    useEffect(() => {
        socket.on("room_list", (data) => {
            setRooms(data['rooms']);
            setChatooms(data['rooms']);
        });
    
        return () => {
            socket.off("room_list");
        };
    }, []);


    useEffect(() => {
        socket.on("user_data", (data) => {
            const profilePreview = document.querySelector('.profile_user_preview');
            const profileButton = document.getElementById('profile_button');
            // const profileStatus = profilePreview.querySelector('.profile_status');
            profileButton.src = data["profile"] ? data["profile"] : "/icons/favicon.ico";
            profilePreview.querySelector('p').innerHTML = data["displayName"];
            // profileStatus.querySelector('div').style.background = data["status"] === 'online' ? 'lime' : 'red';
            // profileStatus.querySelector('p').innerHTML = data["status"];
        });
    
        return () => {
            socket.off("user_data");
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

    function updateChatRoom(roomid,  room_name) {
      const room_display = document.getElementById("room_display");
      rid = roomid;
      room_display.innerHTML = room_name;
    }

    window.addEventListener('popstate', (event) => {
        const roomName = event.state ? event.state.roomName : 'Main';
        updateChatRoom(rid, roomName);
    });
  

    // document.addEventListener('DOMContentLoaded', () => {
    //   const currentRoom = window.location.pathname.split('/')[2] || 'Main';
    //   updateChatRoom(rid ,currentRoom);
    // //   socket.emit("join_room", { roomid: 'ilQvQwgOhm9kNAOrRqbr', suuid: suuid });
    // })
  
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
            <div className='profile_card'>
                <div className='profile_preview'>
                    <img className='profile_button' alt='profile' src='/icons/favicon.ico'/>
                    <div className='profile_user_preview'>
                        <p>User #1</p>
                        <div className='profile_status'>
                            <div style={{background: "lime"}}></div>
                            <p>Online</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className='sidenav_dropdown'>
                <div className='sidenav_button'>
                <FontAwesomeIcon icon={faBorderAll}/>
                <p>Chat Rooms</p>
                </div>
                <ul className='sidenav_dropdown content' id='room_list'>
                    {rooms.map(([name, value], index) => (
                        <li key={index} onClick={() => changeChatRoom(value, name)}>
                            {name}
                        </li>
                    ))}
                </ul>
            </div>
  
            <a href='/settings' className='sidenav_button'>
                <FontAwesomeIcon icon={faGear}/>
                <p>Settings</p>
            </a>
            <a className='sidenav_button' onClick={logout}>
                <FontAwesomeIcon icon={faRightFromBracket} color='red'/>
                <p>Logout</p>
            </a>
        </div>
  
        <div className='chat_container'>
            <div className='topbar'>
                <div>
                    <button onClick={() => open_sidenav()} id='nav_button'>
                    <FontAwesomeIcon icon={faBars}/>
                    </button>
                    <h2 id='room_display'>loading...</h2>
                </div>

                <div className='profile_card'>
                    <div className='profile_preview'>
                        <img className='profile_button' id='profile_button' src='/icons/favicon.ico'/>
                        <div className='profile_user_preview'>
                            <p>loading...</p>
                            <div className='profile_status'>
                                <div style={{background: "lime"}}></div>
                                <p>Online</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div className='main_chat_body'>
                <div className='chat' id='chat'>
                </div>
    
                <div className='user_list'>
                    <input type='text' placeholder='Search for a user' id='user_search_input'/>
                    <div id='user_list'>
                        {user_data["data"] ? (
                            Object.entries(user_data["data"]).map(([key, user], index) => (
                                <SetUsersList user_name={user["displayName"]} profile_picture={user["profile"]} user_role={user["role"]} key={index} status={ par_user['data']['uuid'] === user['uuid'] ? ostatus : user['status']}/>
                            ))
                        ) : (
                            <p>Fetching Data</p>
                        )}
                    </div>
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
                    spellCheck='true'
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            sendMessage();
                        }
                    }}
                    />
                <button 
                    id='send_button' 
                    onClick={sendMessage}>
                <FontAwesomeIcon icon={faPaperPlane}/>
                </button>
            </div>
            </div>
        </div>

        <div className='background_blur'>
            <div className='user_profile_modal'>
                <div className='profile_modal_options'>
                <div className='profile_modal_button'>
                        <span>
                            <FontAwesomeIcon icon={faUserPlus}/>
                            <p>Add Friend</p>
                        </span>
                        <FontAwesomeIcon icon={faChevronRight}/>
                    </div>

                    <div className='profile_modal_button'>
                        <span>
                            <FontAwesomeIcon icon={faMessage}/>
                            <p>DM</p>
                        </span>
                        <FontAwesomeIcon icon={faChevronRight}/>
                    </div>
                </div>

                <div className='profile_details'>
                    <button className='close_modal_button'>
                        <FontAwesomeIcon icon={faXmark}/>
                    </button>
                    <div className='modal_user_details'>
                        <img src={null} id='modal_user_picture'/>
                        <div className='modal_extra_details'>
                            <h1 id='modal_user_name'>Display Name</h1>
                            <p id='modal_user_role'>Role</p>
                        </div>
                    </div>
                    <div className='modal_badge_list'>
                        <p className=' badge admin'>admin</p>
                        <p className='badge mod'>OG Badge</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    )
}
  
export default Chat


