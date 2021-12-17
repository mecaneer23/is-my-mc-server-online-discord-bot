#!/bin/python3
import json
import time, datetime
import discord
from mcstatus import MinecraftServer
import requests

#general setup
with open("env.json", 'r') as env_file:
    env = json.load(env_file)
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
output_log = True
log_file = None


def olprint(message):  # output log print
    if output_log == True:
        print(f"{message}\n")
        if log_file != None:
            log_file.write(f"{message}\n")


@client.event
async def on_ready():
    olprint(f"Bot online with user: {client.user}\n")
    botActivity = discord.Activity(type=discord.ActivityType.watching,
                                   name='for ;server')
    await client.change_presence(activity=botActivity)
    time.sleep(1)


@client.event
async def on_message(message):
    color = int(
        str(message.guild.get_member(client.user.id).roles[-1].color)[1:], 16)
    if message.content.lower().startswith(";server"):
        try:
            port = message.content.split(" ")[2]
        except IndexError:
            port = 25565
        try:
            server = message.content.split(" ")[1]
        except IndexError:
            olprint(f"{message.author} failed to include server")
            await message.channel.send(embed=discord.Embed(
                title="Bad Argument",
                color=color,
                description=
                "Error: make sure to include a server and optional port - for example:\n```\n;server mc.server.net[ 12345]\n```"
            ))
            return
        olprint(
            f"{str(datetime.datetime.now())}\n{message.author}: Pinging {server}"
        )
        try:
            if server == "tcwe.apexmc.co":
                status = MinecraftServer(server, 25633).status()
            else:
                status = MinecraftServer(server, port).status()
        except OSError as e:
            if str(e) == "timed out":
                olprint(f"Invalid server address or request timed out")
                await message.channel.send(embed=discord.Embed(
                    title="Server Info",
                    color=color,
                    description=
                    "Error: Invalid server address or request timed out"))
            else:
                olprint(f"Server failed to respond: {e}")
                await message.channel.send(
                    embed=discord.Embed(title="Server Info",
                                        color=color,
                                        description=f"Error: {e}"))
            return
        except Exception as e:
            olprint(f"Hmm... I don't know what this error is: {e}")
            await message.channel.send(embed=discord.Embed(
                title="Server Info", color=color, description=f"Error: {e}"))
            return

        online = status.players.online
        temp = requests.get(f"https://api.mcsrvstat.us/2/{server}").json()
        try:
            if temp["players"]["online"] != 0:
                query = temp["players"]["list"]
            else:
                query = ""
        except KeyError as e:
            olprint(f"Server failed to respond: {e}")
            await message.channel.send(embed=discord.Embed(
                title="Server Info",
                color=color,
                description=
                f"Error: Possibly incorrect port, contact the server admins to learn more"
            ))
            return
        players = ""
        for i in query:
            players += i + "\n"
        olprint(f"There are {str(online)} players online:\n{players or '...'}")
        await message.channel.send(embed=discord.Embed(
            title="Server Info", color=color
        ).add_field(
            name=f"There are {str(online)} players online:",
            value=players or "..."
        ).set_footer(
            text=
            "Due to inconsistent APIs, the player names may not always be correct"
        ))


client.run(env["DISCORD_TOKEN"])
