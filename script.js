function setName() {
	localStorage.setItem("name", document.getElementById("in-name").value);
	window.location.href = "/chat";
}