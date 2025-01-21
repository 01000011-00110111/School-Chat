/**
 * Oh my where even to start
 */
const context_menu = {
    /**
     * Creates the context menu
     * @argument {options} Adds the provided objects as menu options
     * @argument {attach} Attaches the menu to a parent html element
     */
    generate: function(options = {}, attach, left, right, top, bottom) {
        const menu = document.createElement("div");
        menu.classList.add("native_context_menu");

        if (right) {
            menu.style.left = `${right + 5}px`;
        }
        
        if (left) {
            menu.style.left = `${left - right - 5}px`;
        }
        
        if (top) {
            menu.style.top = `${top + 5}px`;
        }
        
        if (bottom) {
            menu.style.top = `${bottom - top - 5}px`;
        }
        
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


const handle_create = (event, options = {}) => {
    const clickX = event.clientX;
    const clickY = event.clientY;
    const screenW = window.innerWidth;
    const screenH = window.innerHeight;

    const right = (screenW - clickX);
    const left = !right;
    const top = (screenH - clickY);
    const bottom = !top;

    console.log(clickX + " : " + clickY)

    event.preventDefault();

    context_menu.generate(options, document.body, left, top)
}

export {context_menu, handle_create};