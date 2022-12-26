import nextcord
from nextcord import Button, ButtonStyle, Embed, Interaction, SlashOption
from nextcord.ext import commands
import random

import formatted_stats
import utils

TOKEN = "MTA1NjYwNzA3ODgyOTAxOTE1Ng.GbR4Qj.UyR2DBWS3RKJRssD6bNHgsxloe96QLhudLsHdU"
guild_ids = [977351156202356757, 1009941602317385781, 849345805604618270, 1056611873455341739, 1026725257505161236, 734897964400771193]

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

@client.slash_command(guild_ids=guild_ids, description="Focus blast")
async def focus_blast(interaction: Interaction):
    # thirty percent chance to send the message "Focus miss" and 70% chance to send the message "Focus blast"
    if random.randint(1, 10) <= 3:
        await interaction.response.send_message("Focus miss")
    else:
        await interaction.response.send_message("Focus blast")

client.run(TOKEN)