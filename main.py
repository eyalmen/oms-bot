import random
import json

import nextcord
from nextcord import Button, ButtonStyle, Embed, Interaction, SlashOption
from nextcord.ext import commands

import formatted_stats
import utils

TOKEN = ""
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
    stat: str = SlashOption(description="The stat to get", choices=["used", "winrate", "lead", "abilities", "items", "moves", "partners"]),
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

@client.slash_command(guild_ids=guild_ids, description="Focus blast")
async def focus_blast(interaction: Interaction):
    # thirty percent chance to send the message "Focus miss" and 70% chance to send the message "Focus blast"
    if random.randint(1, 10) <= 3:
        await interaction.response.send_message("Focus miss")
    else:
        await interaction.response.send_message("Focus blast")

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