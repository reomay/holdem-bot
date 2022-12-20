import discord
from discord import app_commands
from discord.ext import commands

guild_object = discord.Object(id=1024623147124797450)

class ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="show latency of bot",
    )
    async def ping_command(self,
                           interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Latency",
                description=f"`{round(self.bot.latency * 1000)}ms`",
                color=0x62c1cc
            )
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        ping(bot),
        guild=guild_object
    )