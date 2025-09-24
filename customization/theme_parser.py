"""theme_parser.py: Main webserver file for school-chat, a chat server
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import random

def create_theme_id():
    """Creates a random 12 digit id to associate with a theme"""
    tid : str = ""
    id_length: int = 0
    reset_buffer: int = 0

    char_amount: int = 12

    while id_length < char_amount:
        if reset_buffer == 3:
            tid += "_"
            reset_buffer = 0

        tid += str(random.randint(1, 9))

        id_length += 1
        reset_buffer += 1

    return tid

def transform_theme(data: list):
    """Converts the cff file format into a dictionary."""
    section = ""

    items_dictionary = {
        "headers": {
            "name": "",
            "author": "",
            "version": ""
        },
        "colors": {
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
    }

    items: str = ""
    for items in data:
        if "[Header]" in items:
            section = "headers"

        elif "[Colors]" in items:
            section = "colors"

        key = items.replace("\n", "").split(":", 1)[0]
        value = items.replace(" ", "").replace("\n", "").split(":", 1)[-1]


        if ":" in items:
            items_dictionary[section][key] += value

    return items_dictionary
