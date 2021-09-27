from os import name
import discord
from discord.enums import try_enum
from discord.ext import commands
from decouple import config
import requests
from discord.utils import get
from tasks import verification

baseurl = config("BASEAPI")
securetyToken = config("SECURITY_TOKEN")
authorization = config("AUTHORIZATION")


class Role(commands.Cog):
    """Atribute role to user"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            isinstance(message.channel, discord.channel.DMChannel)
            and message.author != self.bot.user
        ):
            if verification.Verify.verify_email(message.content) is not True:
                await message.channel.send("Email invalido!")
                return

            try:
                embed = discord.Embed(
                    title="Estamos verficando seu email, só um momento",
                    color=discord.Color.orange(),
                )
                await message.channel.send(embed=embed)

                acess_headers = {
                    "Authorization": authorization,
                }

                acessResponse = await get_token(acess_headers)

                acessContent = acessResponse.json()
                acessToken = acessContent["access_token"]

                list_headers = {"Authorization": f"Bearer {acessToken}"}

                result = await main_request(baseurl, list_headers, config("NEXT_PAGE"))

                total = result["page_info"]["total_results"]
                perPage = result["page_info"]["results_per_page"]
                nextPage = config("NEXT_PAGE")

                for i in range((total // perPage) + 1):
                    print(i)
                    if i != 0:
                        nextPage = get_pages(nextPage)
                    request = await main_request(baseurl, list_headers, nextPage)
                    nextPage = request
                    response = get_result(request, message.content.lower())
                    if response:
                        userId = message.author.id
                        guildId = int(config("GUILD_ID"))
                        guild = self.bot.get_guild(guildId)
                        member = await guild.fetch_member(userId)
                        role_id = int(config("ROLE_ID"))
                        role = get(guild.roles, id=role_id)
                        if member:
                            await member.add_roles(role)
                            embed2 = discord.Embed(
                                title="Registrado!", color=discord.Color.green()
                            )
                            embed2.set_footer(
                                text=f"Parabens {response['name']}, você está registrado e pode aproveitar as funcionalidade premium da comunidade"
                            )
                            await message.channel.send(embed=embed2)
                            break
                else:
                    communityName = "Sociedade do Código"
                    embed3 = discord.Embed(
                        title="Você não está registrado!", color=discord.Color.red()
                    )
                    embed3.set_footer(
                        text=f"Adquira a {communityName} para ter acesso a funções premium."
                    )
                    await message.channel.send(embed=embed3)

            except discord.errors.Forbidden:
                await message.channel.send("Erro! tente novamente.")


async def get_token(acess_headers):
    try:
        request = requests.post(
            securetyToken,
            headers=acess_headers,
        )
        return request
    except requests.exceptions.HTTPError as error:
        print(error)


def get_result(response, message):
    for item in response["items"]:
        if item["email"] == message:
            return item


def get_pages(result):
    return result["page_info"]["next_page_token"]


async def main_request(baseurl, header, x=config("NEXT_PAGE")):
    try:
        r = requests.get(baseurl + f"&page_token={x}", headers=header)
        return r.json()
    except requests.exceptions.HTTPError as error:
        print(error)


def setup(bot):
    bot.add_cog(Role(bot))
