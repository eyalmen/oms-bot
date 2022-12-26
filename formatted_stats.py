import json

def get_stats(path):
    with open(path) as f:
        stats = json.load(f)
    return stats

def get_all_stats(path, pokemon):
    stats = get_stats(path)
    stats = stats["pokemon"]
    
    wanted_stats = {
        "used": stats[pokemon]["usage"]["real"],
        "win": stats[pokemon]["win"]["real"],
        "lead": stats[pokemon]["lead"]["real"],
        "abilities": stats[pokemon]["abilities"],
        "partners": stats[pokemon]["teammates"],
        "moves": stats[pokemon]["moves"],
        "items": stats[pokemon]["items"],
        # TODO: nm and spread
    }

    return wanted_stats

def get_formatted_stats(path, pokemon):
    stats = get_all_stats(path, pokemon)
    formatted_stats = {
        "used": f"**Used:** {stats['used']}%",
        "win": f"**Win:** {stats['win']}%",
        "lead": f"**Lead:** {stats['lead']}%",  
        # "abilities": f"**Abilities:** {'\n'.join([f'''{ability}: {stats['abilities'][ability]}''' for ability in stats['abilities']])}",
        # "partners": f"**Partners:** {'\n'.join([f'''{partner}: {stats['partners'][partner]}''' for partner in stats['partners']])}",
        # "moves": f"**Moves:** {'\n'.join([f'''{move}: {stats['moves'][move]}''' for move in stats['moves']])}",
        # "items": f"**Items:** {'\n'.join([f'''{item}: {stats['items'][item]}''' for item in stats['items']])}",
    }
    # you can't have backsplashes in f-strings
    formatted_stats["abilities"] = "**Abilities:**" + '\n'.join([f'''{ability}: {stats['abilities'][ability]}''' for ability in stats['abilities']])
    formatted_stats["partners"] = "**Partners:**" + '\n'.join([f'''{partner}: {stats['partners'][partner]}''' for partner in stats['partners']])
    formatted_stats["moves"] = "**Moves:**" + '\n'.join([f'''{move}: {stats['moves'][move]}''' for move in stats['moves']])
    formatted_stats["items"] = "**Items:**" + '\n'.join([f'''{item}: {stats['items'][item]}''' for item in stats['items']])
    return formatted_stats