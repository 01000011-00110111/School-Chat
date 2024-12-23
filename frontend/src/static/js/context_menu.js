/**
 * Oh my where even to start
 */
const context_menu = {
    /**
     * Creates the context menu
     * @argument {options} Adds the provided objects as menu options
     * @argument {attach} Attaches the menu to a parent html element
     */
    generate: function(options = {}, attach) {
        const menu = document.createElement("div");
        for (const [key, value] of Object.entries(options)) {
            const button = document.createElement("button");
            button.innerHTML = key;

            button.onclick = function() {
                console.log(value);
            }
            menu.appendChild(button);
        }
        attach.appendChild(menu);
        return 0;
    },

    get_all_instances: function() {
        return 0;
    },

    destroy: function() {

    }
}

export default context_menu;