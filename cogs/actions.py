import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

# API pública gratuita de gifs de anime para comandos de acción.
# Documentación: https://docs.nekos.best
NEKOS_BEST = "https://nekos.best/api/v2"


class Actions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_gif(self, categoria: str) -> str:
        headers = {"User-Agent": "DiscordBotDePruebas/1.0 (https://github.com)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{NEKOS_BEST}/{categoria}") as resp:
                if resp.status != 200:
                    print(f"⚠️ nekos.best devolvió status {resp.status} para {categoria}")
                    return None
                data = await resp.json()
                return data["results"][0]["url"]

    async def send_action(self, interaction: discord.Interaction, categoria: str, verbo: str, usuario: discord.Member):
        """Comandos dirigidos a otra persona: /slap @fulano"""
        await interaction.response.defer()
        try:
            url = await self.get_gif(categoria)
        except Exception as e:
            print(f"⚠️ Error en send_action ({categoria}): {type(e).__name__}: {e}")
            await interaction.followup.send(f"❌ Error trayendo el gif: `{type(e).__name__}: {e}`")
            return

        if not url:
            await interaction.followup.send("❌ La API no devolvió ninguna imagen, intenta de nuevo.")
            return

        if usuario.id == interaction.user.id:
            texto = f"{interaction.user.mention} se {verbo} a sí mismo 💀"
        else:
            texto = f"{interaction.user.mention} le {verbo} a {usuario.mention}"

        try:
            embed = discord.Embed(color=discord.Color.blurple())
            embed.set_image(url=url)
            await interaction.followup.send(content=texto, embed=embed)
        except Exception as e:
            print(f"⚠️ Error enviando embed ({categoria}): {type(e).__name__}: {e}")
            await interaction.followup.send(f"{texto}\n{url}")

    async def send_expression(self, interaction: discord.Interaction, categoria: str, verbo: str):
        """Comandos sin objetivo: /dance, /cry, etc."""
        await interaction.response.defer()
        try:
            url = await self.get_gif(categoria)
        except Exception as e:
            print(f"⚠️ Error en send_expression ({categoria}): {type(e).__name__}: {e}")
            await interaction.followup.send(f"❌ Error trayendo el gif: `{type(e).__name__}: {e}`")
            return

        if not url:
            await interaction.followup.send("❌ La API no devolvió ninguna imagen, intenta de nuevo.")
            return

        try:
            embed = discord.Embed(color=discord.Color.blurple())
            embed.set_image(url=url)
            await interaction.followup.send(content=f"{interaction.user.mention} {verbo}", embed=embed)
        except Exception as e:
            print(f"⚠️ Error enviando embed ({categoria}): {type(e).__name__}: {e}")
            await interaction.followup.send(f"{interaction.user.mention} {verbo}\n{url}")

    # ---------- Comandos dirigidos a otra persona ----------

    @app_commands.command(name="slap", description="Le das una cachetada a alguien")
    @app_commands.describe(usuario="A quién le pegas")
    async def slap(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "slap", "dio una cachetada", usuario)

    @app_commands.command(name="hug", description="Le das un abrazo a alguien")
    @app_commands.describe(usuario="A quién abrazas")
    async def hug(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "hug", "abrazó", usuario)

    @app_commands.command(name="kiss", description="Le das un beso a alguien")
    @app_commands.describe(usuario="A quién besas")
    async def kiss(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "kiss", "besó", usuario)

    @app_commands.command(name="pat", description="Le das cariñitos en la cabeza a alguien")
    @app_commands.describe(usuario="A quién le das cariñitos")
    async def pat(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "pat", "le dio cariñitos a", usuario)

    @app_commands.command(name="cuddle", description="Te acurrucas con alguien")
    @app_commands.describe(usuario="Con quién te acurrucas")
    async def cuddle(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "cuddle", "se acurrucó con", usuario)

    @app_commands.command(name="poke", description="Le das un empujoncito a alguien")
    @app_commands.describe(usuario="A quién empujas")
    async def poke(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "poke", "le dio un empujoncito a", usuario)

    @app_commands.command(name="bite", description="Le das una mordida a alguien")
    @app_commands.describe(usuario="A quién muerdes")
    async def bite(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "bite", "le dio una mordida a", usuario)

    @app_commands.command(name="feed", description="Le das de comer a alguien")
    @app_commands.describe(usuario="A quién alimentas")
    async def feed(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "feed", "le dio de comer a", usuario)

    @app_commands.command(name="highfive", description="Le chocas los cinco a alguien")
    @app_commands.describe(usuario="A quién le chocas los cinco")
    async def highfive(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "highfive", "le chocó los cinco a", usuario)

    @app_commands.command(name="punch", description="Le das un puñete a alguien")
    @app_commands.describe(usuario="A quién le pegas")
    async def punch(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "punch", "le dio un puñete a", usuario)

    @app_commands.command(name="tickle", description="Le haces cosquillas a alguien")
    @app_commands.describe(usuario="A quién le haces cosquillas")
    async def tickle(self, interaction: discord.Interaction, usuario: discord.Member):
        await self.send_action(interaction, "tickle", "le hizo cosquillas a", usuario)

    # ---------- Comandos de expresión (sin objetivo) ----------

    @app_commands.command(name="dance", description="Bailas")
    async def dance(self, interaction: discord.Interaction):
        await self.send_expression(interaction, "dance", "está bailando 💃")

    @app_commands.command(name="cry", description="Lloras")
    async def cry(self, interaction: discord.Interaction):
        await self.send_expression(interaction, "cry", "está llorando 😢")

    @app_commands.command(name="blush", description="Te sonrojas")
    async def blush(self, interaction: discord.Interaction):
        await self.send_expression(interaction, "blush", "se sonrojó 😳")

    @app_commands.command(name="smile", description="Sonríes")
    async def smile(self, interaction: discord.Interaction):
        await self.send_expression(interaction, "smile", "está sonriendo 🙂")

    @app_commands.command(name="laugh", description="Te ríes")
    async def laugh(self, interaction: discord.Interaction):
        await self.send_expression(interaction, "laugh", "se está riendo 😂")

    @app_commands.command(name="wave", description="Saludas")
    async def wave(self, interaction: discord.Interaction):
        await self.send_expression(interaction, "wave", "está saludando 👋")

    @app_commands.command(name="wink", description="Guiñas el ojo")
    async def wink(self, interaction: discord.Interaction):
        await self.send_expression(interaction, "wink", "guiñó el ojo 😉")

    @app_commands.command(name="thumbsup", description="Das el visto bueno")
    async def thumbsup(self, interaction: discord.Interaction):
        await self.send_expression(interaction, "thumbsup", "dio el visto bueno 👍")

    # ---------- Dado ----------

    @app_commands.command(name="dado", description="Tira un dado de 6 caras (o el número de caras que quieras)")
    @app_commands.describe(caras="Número de caras del dado (por defecto 6)")
    async def dado(self, interaction: discord.Interaction, caras: int = 6):
        if caras < 2:
            await interaction.response.send_message("❌ El dado necesita al menos 2 caras.", ephemeral=True)
            return
        resultado = random.randint(1, caras)
        await interaction.response.send_message(f"🎲 Tiraste un dado de {caras} caras: **{resultado}**")


async def setup(bot: commands.Bot):
    await bot.add_cog(Actions(bot))
