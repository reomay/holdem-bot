import discord
from discord import app_commands
from discord.ext import commands
from dataclasses import dataclass
import random

guild_object = discord.Object(id=1024623147124797450)

ingame: list = [

]


class my_hand_button(discord.ui.View):
    def __init__(self, *, hands: list, author_id: int) -> None:
        super().__init__(timeout=None)
        self.hands = hands
        self.author_id = int(author_id)

    @discord.ui.button(label="눌러서 패 보기", style=discord.ButtonStyle.gray)
    async def hand_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.author_id == int(interaction.user.id):
            embed: discord.Embed = discord.Embed( # author
                title="당신의 패",
                description=f"{self.hands[0][0]}, {self.hands[0][1]}"
            )
        else:
            embed: discord.Embed = discord.Embed( # other
                title="당신의 패",
                description=f"{self.hands[1][0]}, {self.hands[1][1]}"
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
class bet(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="bet", style=discord.ButtonStyle.green)
    async def bet_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
class bet_raise(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="raise", style=discord.ButtonStyle.green)
    async def raise_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
class fold(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="raise", style=discord.ButtonStyle.red)
    async def fold_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
class call(discord.ui.View):
    def __init__(self, *, hands: list, author_id: int) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="call", style=discord.ButtonStyle.green)
    async def call_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass


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

    def pop_card(self) -> str:
        pop_card: str = self.__deck[0]
        del self.__deck[0]
        self._droped_cards.append(pop_card)
        return pop_card

    def get_deck(self) -> list:
        return self.__deck


class Holdem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="홀덤",
        description="홀덤 게임을 시작합니다.",
    )
    async def holdem_command(self,
                             interaction: discord.Interaction,
                             other:discord.User=None) -> None:

        #card settings
        deck:Card = Card()
        deck.shuffle()

        field_data: dict = {
            "author_chips": 19,
            "other_chips": 19,
            "field_POT": 2,
            "author_raised": 0,
            "other_raised": 0
        }

        hands: list = [[deck.pop_card(), deck.pop_card()], [deck.pop_card(), deck.pop_card()]] # hands[0] = author, hands[1] = other



        ingame.append({
            "player": {
                str(interaction.user.id): { #author data
                    "hand": hands[0]
                },
                str(other.id): { #other data
                    "hand": hands[1]
                }
            }
        })


        await interaction.response.send_message(
            embed=discord.Embed(
                title="게임 시작",
                color=0x62c1cc
            ),
            view=my_hand_button(hands=hands, author_id=interaction.user.id),
        )

        while True:
            await interaction.channel.send(
                embed=discord.Embed(
                    title=f"{interaction.user.mention} 님의 베팅 차례입니다.",
                    description=f"남은칩:{field_data.get('author_chips')}, POT{field_data.get('field_POT')}",
                    color=0x00FF00
                ),
                views=[my_hand_button(hands=hands, author_id=interaction.user.id), ]
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Holdem(bot),
        guild=guild_object
    )