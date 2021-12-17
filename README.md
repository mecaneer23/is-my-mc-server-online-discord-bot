# Is My Minecraft Server Online Discord Bot

This is a discord bot which can ping a minecraft server to
determine whether it is online or not and who, if anyone, is online.

## Install

- Clone this repository
- make sure pip is installed
- pip install the required dependencies
  - mcstatus
  - discord
- create a file called env.json
- add one field to that file, which is a discord bot token

```bash

git clone https://github.com/Mecaneer23/is-my-mc-server-online-discord-bot.git
# optional pip download on Linux:
#     sudo apt install python3-pip
#     sudo pacman -S python-pip
pip install mcstatus discord
ed
a
{
    "DISCORD_TOKEN": ""
}
.
w env.json
q
python[3] bot.py

```
