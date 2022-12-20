import discord
from discord import app_commands
from discord.ext import commands
from dataclasses import dataclass
import random

guild_object = discord.Object(id=1024623147124797450)

@dataclass(kw_only=True)
class Card:
    def __init__(self):
        self.__deck: list = [
            # spades
            "sa",
            "s1",
            "s2",
            "s3",
            "s4",
            "s5",
            "s6",
            "s7",
            "s8",
            "s9",
            "st",
            "sj",
            "sq",
            "sk",
            # hearts
            "ha",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "h7",
            "h8",
            "h9",
            "ht",
            "hj",
            "hq",
            "hk",
            # diamonds
            "da",
            "d1",
            "d2",
            "d3",
            "d4",
            "d5",
            "d6",
            "d7",
            "d8",
            "d9",
            "dt",
            "dj",
            "dq",
            "dk",
            # clovers
            "ca",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5",
            "c6",
            "c7",
            "c8",
            "c9",
            "ct",
            "cj",
            "cq",
            "ck",
        ]
        self._droped_cards: list = list()

    def shuffle(self) -> None:
        random.shuffle(self.__deck)

    def burning(self) -> None:
        top_card: str = self.__deck[0]
        del self.__deck[0]
        self._droped_cards.append(top_card)

    def pop_card(self) -> str:
        pop_card: str = self.__deck[0]
        del self.__deck[0]

        self._droped_cards.append(pop_card)

        return pop_card

    def return_deck(self) -> list:
        return self.__deck


class Holdem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="holdem",
        description="open thread",
    )
    @app_commands.choices(command_type=[
        discord.app_commands.Choice(name="start", value="start"),
        discord.app_commands.Choice(name="bet", value="bet"),
        discord.app_commands.Choice(name="fold", value="fold"),
        discord.app_commands.Choice(name="check", value="check")
    ])
    async def holdem_command(self,
                             interaction: discord.Interaction,
                             command_type: app_commands.Choice[str], other_person:discord.User=None) -> None:

        if command_type.value == "start":
            channel = await interaction.channel.create_thread(name="asdf", type=discord.ChannelType.public_thread)

            #invite users
            await channel.add_user(interaction.user)
            await channel.add_user(other_person)

            deck = Card()

        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"test",
                description=f"{command_type.value}"
            )
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Holdem(bot),
        guild=guild_object
    )