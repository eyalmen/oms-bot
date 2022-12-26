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
        "winrate": stats[pokemon]["win"]["real"],
        "lead": stats[pokemon]["lead"]["real"],
        "abilities": stats[pokemon]["abilities"],
        "partners": stats[pokemon]["teammates"],
        "moves": stats[pokemon]["moves"],
        "items": stats[pokemon]["items"],
        # TODO: nm and spread
    }

    return wanted_stats

def get_formatted_stats(path, pokemon, cutoff = -1):
    stats = get_all_stats(path, pokemon)
    
    formatted_stats = {
        "used": f"{round(stats['used']*100, 3)}%",
        "winrate": f"{round(stats['winrate']*100, 3)}%",
        "lead": f"{round(stats['lead']*100, 3)}%",
        # "abilities": f"**Abilities:** {'\n'.join([f'''{ability}: {stats['abilities'][ability]}''' for ability in stats['abilities']])}",
        # "partners": f"**Partners:** {'\n'.join([f'''{partner}: {stats['partners'][partner]}''' for partner in stats['partners']])}",
        # "moves": f"**Moves:** {'\n'.join([f'''{move}: {stats['moves'][move]}''' for move in stats['moves']])}",
        # "items": f"**Items:** {'\n'.join([f'''{item}: {stats['items'][item]}''' for item in stats['items']])}",
    }
    # you can't have backsplashes in f-strings
    # include cutoff
    formatted_stats["abilities"] = '\n'.join([f'''{ability}: {round(stats['abilities'][ability] * 100, 3)}%''' for ability in stats['abilities']])
    formatted_stats["partners"] = '\n'.join([f'''{partner}: {round(stats['partners'][partner] * 100, 3)}%''' for partner in stats['partners']])
    formatted_stats["moves"] = '\n'.join([f'''{move}: {round(stats['moves'][move] * 100, 3)}%''' for move in stats['moves']])
    formatted_stats["items"] = '\n'.join([f'''{item}: {round(stats['items'][item] * 100, 3)}%''' for item in stats['items']])

    if cutoff > 0:
        formatted_stats["abilities"] = '\n'.join(formatted_stats["abilities"].split('\n')[:cutoff])
        formatted_stats["partners"] = '\n'.join(formatted_stats["partners"].split('\n')[:cutoff])
        formatted_stats["moves"] = '\n'.join(formatted_stats["moves"].split('\n')[:cutoff])
        formatted_stats["items"] = '\n'.join(formatted_stats["items"].split('\n')[:cutoff])
        
    return formatted_stats