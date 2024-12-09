let suuid = '';

function setSuuid(sessionUUID) {
    suuid = sessionUUID;
    sessionStorage.setItem("suuid", sessionUUID);
}

export { setSuuid, suuid };
