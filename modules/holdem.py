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
            "♠A",
            "♠2",
            "♠3",
            "♠4",
            "♠5",
            "♠6",
            "♠7",
            "♠8",
            "♠9",
            "♠10",
            "♠J",
            "♠Q",
            "♠K",
            # hearts
            "♥A",
            "♥2",
            "♥3",
            "♥4",
            "♥5",
            "♥6",
            "♥7",
            "♥8",
            "♥9",
            "♥10",
            "♥J",
            "♥Q",
            "♥K",
            # diamonds
            "♦A",
            "♦2",
            "♦3",
            "♦4",
            "♦5",
            "♦6",
            "♦7",
            "♦8",
            "♦9",
            "♦10",
            "♦J",
            "♦Q",
            "♦K",
            # clovers
            "♣A",
            "♣2",
            "♣3",
            "♣4",
            "♣5",
            "♣6",
            "♣7",
            "♣8",
            "♣9",
            "♣10",
            "♣J",
            "♣Q",
            "♣K",
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
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Holdem",
                description="```please check your dm.```",
                color=0x62c1cc
            )
        )

        if command_type.value == "start":
            #card settings
            deck:Card = Card()
            deck.shuffle()
            author_cards: list = [deck.pop_card(), deck.pop_card()]
            other_person_cards: list = [deck.pop_card(), deck.pop_card()]


            author_dm = await interaction.user.create_dm()
            await author_dm.send(f"{author_cards[0]}, {author_cards[1]}")

            other_person_dm = await other_person.create_dm()
            await other_person_dm.send(f"{other_person_cards[0]}, {other_person_cards[1]}")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Holdem(bot),
        guild=guild_object
    )