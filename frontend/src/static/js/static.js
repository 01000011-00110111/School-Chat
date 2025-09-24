import { useEffect, useState } from "react";
import socket from "../../socket";

socket.on('ping', () => {
    new window.Notification("You have been pinged");
});