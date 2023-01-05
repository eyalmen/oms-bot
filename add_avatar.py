import json
import os
import pathlib

import requests

# changing the server
avatarstsx = pathlib.Path("/200gb/pseudos-showdown/server/chat-commands/avatars.tsx")
official_avatars_start = """const OFFICIAL_AVATARS = new Set([
"""

avatar_types_json = pathlib.Path("/200gb/pseudos-showdown/config/avatar_types.json")

def add_to_tsx(name):
    with open(avatarstsx, "r") as f:
        lines = f.readlines()
    with open(avatarstsx, "w") as f:
        for line in lines:
            if line == official_avatars_start:
                f.write(line)
                f.write(f"    '{name}',\n")
            else:
                f.write(line)

def add_to_avatar_types(name, filepath):
    extension = filepath.split(".")[-1]
    with open(avatar_types_json, "r") as f:
        avatar_types = json.load(f)
    avatar_types[name] = extension

    with open(avatar_types_json, "w") as f:
        json.dump(avatar_types, f, indent=4)

avatars_dir = pathlib.Path("/200gb/pokemon-showdown-client/sprites/trainers")

battle_dex_data_ts = pathlib.Path("/200gb/pokemon-showdown-client/src/battle-dex-data.ts")
add_avatar_to_client_start = """	'#bw2elesa': 'elesa-gen5bw2',
"""

battle_dex_ts = pathlib.Path("/200gb/pokemon-showdown-client/src/battle-dex.ts")
cavatars = """		if (cavatars[avatar]) {
"""

def add_avatar_file(name, url):
    extension = url.split(".")[-1]
    filepath = avatars_dir / f"{name}.{extension}"
    if not filepath.exists():
        print(f"Downloading {name} from {url}")
        r = requests.get(url)
        with open(filepath, "wb") as f:
            f.write(r.content)
    else:
        print(f"File {name} already exists")

def add_avatar_to_client(name):
    with open(battle_dex_data_ts, "r") as f:
        lines = f.readlines()
    
    # find the add_avatar_to_client_start
    # get the line before it
    # on it there is a number preceded by four spaces and followed by a colon
    # get that number + 1
    # replace the add_avatar_to_client_start with "   {number}: '{name}',\n" + add_avatar_to_client_start
    with open(battle_dex_data_ts, "w") as f:
        for line in lines:
            if line == add_avatar_to_client_start:
                previous_line = lines[lines.index(line) - 1]
                number = int(previous_line.split(":")[0].strip()) + 1
                f.write(f"    {number}: '{name}',\n")
                f.write(line)
            else:
                f.write(line)

def add_name_type_to_cavatars(name, path):
    extension = path.split(".")[-1]
    with open(battle_dex_ts, "r") as f:
        lines = f.readlines()
    # replace the line with
    #		cavatars[name] = "<extension>";
    #       <line>
    with open(battle_dex_ts, "w") as f:
        for line in lines:
            if line == cavatars:
                f.write(f'\t\tcavatars["{name}"] = "{extension}";\n')
                f.write(line)
            else:
                f.write(line)

def add_avatar(name, url):
    add_to_tsx(name)
    add_to_avatar_types(name, url)
    add_avatar_file(name, url)
    add_avatar_to_client(name)
    add_name_type_to_cavatars(name, url)
    os.system("cd /200gb/pokemon-showdown-client && node build")
    os.system("cd /200gb/pseudos-showdown && node build")