import nextcord
from nextcord import Button, ButtonStyle, Embed, Interaction, SlashOption
from nextcord.ext import commands

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

    stats = formatted_stats.get_formatted_stats(formats[format], pokemon, cutoff)
    embed = Embed(title=f"{pokemon}", description=f"Stats for {pokemon} in {format}")
    for stat in stats:
        embed.add_field(name=utils.format(stat), value=stats[stat], inline=False)
    await interaction.response.send_message(embed=embed)

client.run(TOKEN)