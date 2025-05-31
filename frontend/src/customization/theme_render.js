export class Theme_System  {
    theme_template = {
        "--main-background-color": "",
        "--chat-background-color": "",
        "--topbar-background-color": "",
        "--topbar-text-color": "",
        "--usercard-text-color": "",
        "--sidenav-background-color": "",
        "--sidenav-text-color": "",
        "--sidenav-buttons-background-color": "",
        "--sidenav-buttons-text-color": "",
        "--bottom-bar-background-color": "",
        "--message-box-background-color": "",
        "--message-box-text-color": "",
        "--send-button-background-color": "",
        "--send-button-text-color": "",
        "--userlist-background-color": "",
        "--userlist-text-color": "",
    }

    render() {
        const root = document.documentElement;

        for (let [key, value] of Object.entries(this.theme_template)) {
            if (value !== undefined) {
                root.style.setProperty(key, value)
            }
            // console.log(key + " : " + value)
        }
    }

    set_theme(theme_values = []) {
        let keys = Object.keys(this.theme_template);

        keys.reduce((acc, key, index) => {
            acc[key] = theme_values[index];
            if (acc[key] !== undefined) {
                this.theme_template = acc;
            }
            return acc
        }, {})
    }
}