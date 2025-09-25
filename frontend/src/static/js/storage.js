// Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

const storage = {
    get: function(item_key, storage_type) {
        if (storage_type === "LOCAL") {
            let fetched_item = window.localStorage.getItem(item_key);

            if (fetched_item) {
                return fetched_item;
            } else {
                setup_storage();
            }
        }

        else if (storage_type === "SESSION") {
            let fetched_item = window.sessionStorage.getItem(item_key);

            if (fetched_item) {
                return fetched_item;
            } else {
                setup_storage();
            }
        }
    },

    set: function(item_key, item_value, storage_type) {
        if (storage_type === "LOCAL") {

            let added_item = window.localStorage.setItem(item_key, item_value)
            return added_item;

        } else if (storage_type === "SESSION") {

            let added_item = window.sessionStorage.setItem(item_key, item_value);
            return added_item;

        }
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

function setup_storage() {
    if (!window.localStorage.getItem("app-nav-settings")) {
        storage.set("app-nav-settings", '{"nav_close_onroom": false}', "LOCAL");
    }

    if (!window.sessionStorage.getItem("user-customization-settings")) {
        storage.set("user-customization-settings", '{"user_theme": ""}', "SESSION");
    }
}

export {storage, setup_storage}