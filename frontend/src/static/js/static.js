import { useEffect, useState } from "react";
import socket from "../../socket";

socket.on('ping', () => {
    window.Notification("You have been pinged")    
});