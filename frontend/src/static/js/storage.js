const nav_settings = window.localStorage.getItem("app-nav-settings");

const storage = {
    get: function(item_key) {
        let fetched_item = window.localStorage.getItem(item_key);
        return fetched_item;
    },

    set: function(item_key, item_value) {
        let added_item = window.localStorage.setItem(item_key, item_value)
        return added_item
    },

    /**
     * Ref aka reference is a way to save retrieved items and edit them
     */
    ref: {
        /**
         * This is a reference to the storage item
         */
        ref_storage: [],

        add: function(item) {
            this.ref_storage.push(item);
            return this.ref_storage;
            
        },

        remove: function(index) {
            this.ref_storage.indexOf(index)
            if (index > -1) {
                this.ref_storage.splice(index, 1);
            }
            return this.ref_storage
        },

        get: function(index) {
            return this.ref_storage[index]
        }
    }
}

// storage.set("app-nav-settings", '{"nav_close_onroom": true}')

export {storage}