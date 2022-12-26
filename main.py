import nextcord
from nextcord import Button, ButtonStyle, Embed, Interaction, SlashOption
from nextcord.ext import commands

TOKEN = "MTA1NjYwNzA3ODgyOTAxOTE1Ng.GbR4Qj.UyR2DBWS3RKJRssD6bNHgsxloe96QLhudLsHdU"
guild_ids = [977351156202356757, 1009941602317385781, 849345805604618270, 1056611873455341739, 1026725257505161236, 734897964400771193]

intents = nextcord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("Bot is now ready for use")
    print("........................")

client.run(TOKEN)