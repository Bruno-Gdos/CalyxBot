import discord
from discord import app_commands
from discord.ext import commands
import os
import youtube

BOT_TOKEN = os.environ['BOT_TOKEN']


def run_discord_bot():
    client = commands.Bot(command_prefix="$", intents = discord.Intents.default())

    @client.event
    async def on_ready():
        print("Calyx is ready.")
        try:
            synced = await client.tree.sync()
            print ("Synced commands: " + str(synced))
        except Exception as e:
            print("Error syncing commands: " + str(e))

    @client.tree.command(name = "youtube" , description = "Downloads the youtube video")
    @app_commands.describe(thing_to_search = "Video Link" )
    async def youtube(interaction: discord.Interaction, thing_to_search: str):
        await interaction.response.send_message(f'{interaction.user.mention}, seu link de download: {youtube.download_link(thing_to_search)}')

    @client.tree.command(name = "hello" , description = "Says hello to the user")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")

    client.run(BOT_TOKEN)
