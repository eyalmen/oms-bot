import json
import random

import nextcord
import requests
from nextcord import Button, ButtonStyle, Embed, Interaction, SlashOption
from nextcord.ext import commands

import add_avatar as addvatar
import formatted_stats
import utils
from ps_ELO import calculateBattle
from ps_GLICKO import Player, updateRating
from ps_GXE import get_gxe

with open("token.json") as f:
    TOKEN = json.load(f)
TOKEN = TOKEN["token"]
guild_ids = [977351156202356757, 1009941602317385781, 849345805604618270, 1056611873455341739, 1026725257505161236, 734897964400771193, 1009941602317385781]

intents = nextcord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("Bot is now ready for use")
    print("........................")

formats = {
    "DNU": "formats/gen9donotuse.json",
    "DNU Suspect": "formats/gen9donotusesuspect.json",
    "UUD": "formats/gen9uud.json",
    "OUD": "formats/gen9oud.json",
}

@client.slash_command(guild_ids=guild_ids, description="Get all of a pokemon's usage stats")
async def get_stats(interaction: Interaction, 
    pokemon: str, 
    format: str = SlashOption(description="The format to get stats from", choices=list(formats.keys())),
    cutoff: int = SlashOption(description="The amount of entries in each stat to show (defaults to all)", default=-1)):

    embed = Embed(title=f"{pokemon}", description=f"Stats for {pokemon} in {format}")

    try:
        stats = formatted_stats.get_formatted_stats(formats[format], pokemon, cutoff)
        for stat in stats:
            embed.add_field(name=utils.format(stat), value=stats[stat], inline=False)
    except KeyError:
        embed.add_field(name="Error", value=f"Invalid pokemon for this format: {pokemon}", inline=False)

    await interaction.response.send_message(embed=embed)

@client.slash_command(guild_ids=guild_ids, description="Get one of a pokemon's usage stats")
async def get_stat(interaction: Interaction,
    pokemon: str,
    stat: str = SlashOption(description="The stat to get", choices=["used", "winrate", "lead", "abilities", "items", "moves", "partners", "users", "spreads"]),
    format: str = SlashOption(description="The format to get stats from", choices=list(formats.keys())),
    cutoff: int = SlashOption(description="The amount of entries in each stat to show (defaults to all)", default=-1)):
    
    embed = Embed(title=f"{pokemon}", description=f"{pokemon}'s {stat.capitalize()} in {format}")

    try:
        stats = formatted_stats.get_formatted_stats(formats[format], pokemon, cutoff = cutoff)
        stat_value = stats[stat]

        embed.add_field(name=utils.format(stat), value=stat_value, inline=False)
    except KeyError:
        embed.add_field(name="Error", value=f"Invalid pokemon for this format: {pokemon}", inline=False)
    await interaction.response.send_message(embed=embed)

@client.slash_command(guild_ids=guild_ids, description="Get the stats of an item")
async def get_item(interaction: Interaction,
    item: str,
    format: str = SlashOption(description="The format to get stats from", choices=list(formats.keys())),
    cutoff: int = SlashOption(description="The amount of entries in each stat to show (defaults to all)", default=-1)):

    embed = Embed(title=f"{item}", description=f"Stats for {item} in {format}")

    try:
        stats = formatted_stats.get_formatted_item_stats(formats[format], item, cutoff)
        for stat in stats:
            embed.add_field(name=utils.format(stat), value=stats[stat], inline=False)
    except KeyError:
        embed.add_field(name="Error", value=f"Invalid item for this format: {item}", inline=False)

    await interaction.response.send_message(embed=embed)

@client.slash_command(guild_ids=guild_ids, description="Get the item leaderboard")
async def get_item_leaderboard(interaction: Interaction,
    format: str = SlashOption(description="The format to get stats from", choices=list(formats.keys())),
    cutoff: int = SlashOption(description="The amount of entries in each stat to show (defaults to all)", default=-1)):

    embed = Embed(title=f"Item Leaderboard", description=f"Item leaderboard for {format}")

    stats = formatted_stats.get_item_leaderboard(formats[format])
    leaderboard = ""
    for item in stats:
        leaderboard += f"{item.capitalize()}: {stats[item]}\n"
    
    if cutoff != -1:
        leaderboard = leaderboard.split("\n")[:cutoff]
        leaderboard = "\n".join(leaderboard)

    embed.add_field(name="Leaderboard", value=leaderboard, inline=False)

    await interaction.response.send_message(embed=embed)

@client.slash_command(guild_ids=guild_ids, description="See who used a pokemon")
async def whoused(interaction: Interaction,
    pokemon: str,
    format: str = SlashOption(description="The format to get stats from", choices=list(formats.keys())),
    cutoff: int = SlashOption(description="The amount of entries in each stat to show (defaults to all)", default=-1)):

    embed = Embed(title=f"{pokemon}", description=f"Users who used {pokemon} in {format}")

    try:
        stats = formatted_stats.get_formatted_stats(formats[format], pokemon, cutoff)
        users = stats["users"]

        embed.add_field(name="Users", value=users, inline=False)
    except KeyError:
        embed.add_field(name="Error", value=f"Invalid pokemon for this format: {pokemon}", inline=False)

    await interaction.response.send_message(embed=embed)

@client.slash_command(guild_ids=guild_ids, description="Add a new avatar to the pseudos client (need to have permission)")
async def add_avatar(interaction: Interaction, avatar: str, url: str):
    # check if the url is valid and the avatar is not in /200gb/pseudos-showdown/config/avatar_types.json as a key
    avatar_types = json.load(open("/200gb/pseudos-showdown/config/avatar_types.json"))
    if not utils.is_valid_url(url) or avatar in avatar_types:
        await interaction.response.send_message("Avatar taken or url invalid")
        return
    
    allowed_users = json.load(open("allowed_users.json"))

    if str(interaction.user.id) in list(allowed_users.keys()):
        await interaction.response.defer()
        addvatar.add_avatar(avatar, url)
        
        avatar_embed = Embed(title="Avatar added", description=f"Avatar {avatar} added with url {url}")
        avatar_embed.set_image(url=url)
        await interaction.followup.send(embed=avatar_embed)
    else:
        await interaction.response.send_message("You do not have permission to add avatars")

@client.slash_command(guild_ids=guild_ids, description="Focus blast")
async def focus_blast(interaction: Interaction):
    # thirty percent chance to send the message "Focus miss" and 70% chance to send the message "Focus blast"
    if random.randint(1, 10) <= 3:
        await interaction.response.send_message("Focus miss")
    else:
        await interaction.response.send_message("Focus blast")

@client.slash_command(guild_ids=guild_ids, description="Calculate GXE from rating and deviation")
async def calc_gxe(interaction: Interaction, rating: int, deviation: int):
    await interaction.response.send_message(f"Your GXE would be {get_gxe(rating, deviation)}%")        

@client.slash_command(guild_ids=guild_ids, description="Calculate elo from a battle")
async def calc_elo(
    interaction: Interaction,
    p1_name: str,
    p1_rating: int,
    p2_name: str,
    p2_rating: int,
    winner: str = SlashOption(description="The winner of the battle", choices=["p1", "p2"]),
    is_local: bool = SlashOption(description="Calculate as if the battle was on the pseudos client or not", default=True)):

    p1 = {"name": p1_name, "elo": p1_rating}
    p2 = {"name": p2_name, "elo": p2_rating}

    score = 1 if winner == "p1" else 0

    new_ratings = calculateBattle(p1, p2, score, local = is_local)
    p1["elo"] = round(new_ratings[0])
    p2["elo"] = round(new_ratings[1])

    # using ansicolors to color the names of the players as purple for p1 and blue for p2 and to show the gain/loss in rating for each player
    # send the message with the new ratings

    ansi_colors = utils.get_ansi_color_codes()

    purple = ansi_colors["purple"]
    blue = ansi_colors["blue"]
    reset = ansi_colors["reset"]
    red = ansi_colors["red"]
    green = ansi_colors["green"]

    message = f"""```ansi
{purple}{p1['name']}: {reset}{p1['elo']} {green}+{p1['elo'] - p1_rating}{reset}
{blue}{p2['name']}: {reset}{p2['elo']} {red}-{p2_rating - p2['elo']}{reset}```
"""

    await interaction.response.send_message(message)

    

@client.slash_command(guild_ids=guild_ids, description="Get the pokemon leaderboard")
async def get_pokemon_leaderboard(interaction: Interaction,
    format: str = SlashOption(description="The format to get stats from", choices=list(formats.keys())),
    cutoff: int = SlashOption(description="The amount of entries in each stat to show (defaults to all)", default=-1)):

    embed = Embed(title=f"Pokemon Leaderboard", description=f"Pokemon usage leaderboard for {format}")

    stats = formatted_stats.get_pokemon_leaderboard(formats[format])
    leaderboard = ""
    for pokemon in stats:
        leaderboard += f"{pokemon.capitalize()}: {stats[pokemon]}\n"
    
    if cutoff != -1:
        leaderboard = leaderboard.split("\n")[:cutoff]
        leaderboard = "\n".join(leaderboard)

    embed.add_field(name="Leaderboard", value=leaderboard, inline=False)

    await interaction.response.send_message(embed=embed)

client.run(TOKEN)