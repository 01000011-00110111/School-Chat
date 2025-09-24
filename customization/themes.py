"""themes.py: Main webserver file for school-chat, a chat server
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
import os
import textwrap
from socketio_confg import sio
from customization.theme_parser import create_theme_id, transform_theme

PATH = "themes"
dir_list = os.listdir(PATH)
print(dir_list)

@sio.on("create_theme")
async def create_theme(sid, author: str, name: str, data: dict, version: str):
    """Creates a theme from the provided arguments"""
    tid = create_theme_id()
    items = ""

    for k,v in data.items():
        items += f"{k}: {v}\r"

    theme_format = f"""
    [Header]
    name: {name}
    author: {author}
    version: {version}

    [Colors]
    {items}
    """

    with open(os.path.join(PATH, tid + ".ccf"), 'w', encoding="utf-8") as fp:
        fp.write(textwrap.dedent(theme_format))


def delete_theme(tid: str):
    """Deletes a theme from the passed ThemeID (tid)"""
    if os.path.exists(os.path.join(PATH, tid + ".ccf")):
        os.remove(os.path.join(PATH, tid + ".ccf"))
        print(f"{tid}.ccf was deleted.")
    else:
        print("That theme does not exist.")

@sio.on("load_theme")
async def load_theme(sid, tid: str):
    """Loads the dictionary version of a theme from the passed ThemeID (tid)"""
    if os.path.exists(os.path.join(PATH, tid + ".ccf")):
        with open(os.path.join(PATH, tid + ".ccf"), 'r', encoding="utf-8") as fp:
            lines = fp.readlines()
            theme = transform_theme(lines)

            await sio.emit("send_theme", {"theme": theme}, to=sid)
    else:
        print(f"The specified file: {tid}.ccf, doesn't exist.")
        await sio.emit("send_theme", {"error": f"The specified file: {tid}.ccf, doesn't exist."}, to=sid)

@sio.on("list_all_themes")
async def list_all_themes(sid):
    """Lists all theme in the themes folder"""
    files = [entry.name for entry in os.scandir(PATH) if entry.is_file()]
    themes: list = []
    for file in files:
        if os.path.exists(os.path.join(PATH, file)):
            with open(os.path.join(PATH, file), 'r', encoding="utf-8") as fp:
                lines = fp.readlines()
                theme = transform_theme(lines)

                themes.append({"name": theme["headers"]["name"], "id": file.split(".ccf")[0]})
                # await sio.emit("returned_themes", {theme["headers"]["author"]: file.split(".ccf")[0]}, to=sid)

    await sio.emit("returned_themes", themes, to=sid)
