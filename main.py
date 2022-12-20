import discord
from discord.ext import commands
from utils import json_handler

guild_object = discord.Object(id=1024623147124797450)


class economy(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents= discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        for command_name in json_handler.Read("config.json")["modules"]:
            await self.load_extension(f"modules.{command_name}")
        await bot.tree.sync(guild=guild_object)

    async def on_ready(self):
        print(f"{self.user.name} has connected to discord!")



bot = economy()
bot.run(json_handler.Read("config.json")["token"])