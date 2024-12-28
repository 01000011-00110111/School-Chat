const nav_settings = window.localStorage.getItem("app-nav-settings");
console.log(JSON.parse(nav_settings));

export {nav_settings}