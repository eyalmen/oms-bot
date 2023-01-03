import json


def get_stats(path):
    with open(path) as f:
        stats = json.load(f)
    return stats

def get_battles(path):
    stats = get_stats(path)
    return stats["battles"]

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
        "users": stats[pokemon]["users"],
        # TODO: nm
        "spreads": stats[pokemon]["spreads"],
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
    formatted_stats["users"] = '\n'.join([f'''{user}: {round(stats['users'][user] * 100, 3)}%''' for user in stats['users']])

    # the average spread string
    # EVs: 248/0/164/0/0/96 IVs: 31/31/31/31/31/31 Timid Nature Level: 100

    formatted_stats["spreads"] = '\n'.join([f'''{spread}: {round(stats['spreads'][spread] * 100, 3)}%''' for spread in stats['spreads']])

    if cutoff > 0:
        abilities = formatted_stats["abilities"].split('\n')
        partners = formatted_stats["partners"].split('\n')
        moves = formatted_stats["moves"].split('\n')
        items = formatted_stats["items"].split('\n')
        users = formatted_stats["users"].split('\n')
        spreads = formatted_stats["spreads"].split('\n')

        users = sorted(users, key=lambda x: float(x.split(':')[1].split('%')[0]), reverse=True)

        formatted_stats["abilities"] = '\n'.join(abilities[:cutoff])
        formatted_stats["partners"] = '\n'.join(partners[:cutoff])
        formatted_stats["moves"] = '\n'.join(moves[:cutoff])
        formatted_stats["items"] = '\n'.join(items[:cutoff])
        formatted_stats["users"] = '\n'.join(users[:cutoff])
        formatted_stats["spreads"] = '\n'.join(spreads[:cutoff])
        
    return formatted_stats

def get_all_items(path):
    stats = get_stats(path)
    stats = stats["items"]
    return stats

def get_item_stats(path, item):
    stats = get_all_items(path)
    item = stats[item]

    item["usage"] = round(item["count"] / get_battles(path) * 100, 3)
    item["winrate"] = round(item["win"] / item["count"] * 100, 3)

    # for every pokemon in item["pokemon"] replace their value with it / item["count"] * 100 rounded to 3 decimal places
    for pokemon in item["pokemon"]:
        item["pokemon"][pokemon] = round(item["pokemon"][pokemon] / item["count"] * 100, 3)

    # sort the pokemon dict by value
    item["pokemon"] = dict(sorted(item["pokemon"].items(), key=lambda x: x[1], reverse=True))

    del item["count"]
    del item["win"]

    return item

def get_formatted_item_stats(path, item, cutoff = -1):
    stats = get_item_stats(path, item)

    formatted_stats = {
        "usage": f"{stats['usage']}%",
        "winrate": f"{stats['winrate']}%",
        "pokemon": '\n'.join([f'''{pokemon}: {stats['pokemon'][pokemon]}%''' for pokemon in stats['pokemon']])
    }

    if cutoff > 0:
        pkmn = formatted_stats["pokemon"].split('\n')
        formatted_stats["pokemon"] = '\n'.join(pkmn[:cutoff])
    
    return formatted_stats

def get_item_leaderboard(path):
    stats = get_all_items(path)

    leaderboard = {}
    for item in stats:
        leaderboard[item] = str(stats[item]["count"]) + f" ({round(stats[item]['count'] / get_battles(path) * 100, 2)}%)"

    # sort by the number before the %)
    leaderboard = sorted(leaderboard.items(), key=lambda x: float(x[1][x[1].index('(')+1:x[1].index('%')]), reverse=True)

    # create a dict from the list of tuples
    leaderboard = dict(leaderboard)

    return leaderboard

def get_pokemon_leaderboard(path):
    stats = get_stats(path)
    stats = stats["pokemon"]

    leaderboard = {}
    for pokemon in stats:
        leaderboard[pokemon] = f"{round(stats[pokemon]['usage']['real'] * 100, 2)}%"

    # sort the dict by the number before the %
    leaderboard = sorted(leaderboard.items(), key=lambda x: float(x[1][:-1]), reverse=True)

    # create a dict from the list of tuples
    leaderboard = dict(leaderboard)

    return leaderboard