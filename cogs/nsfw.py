import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

# API pública de waifu.pics (anime), tiene categoría sfw y nsfw.
# Documentación: https://waifu.pics/docs
BASE_URL = "https://api.waifu.pics/nsfw"

CATEGORIAS = ["waifu", "neko", "trap", "blowjob"]


class NSFW(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def fetch_image(self, categoria: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/{categoria}") as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get("url")

    @app_commands.command(name="nsfw", description="Manda una imagen NSFW random (solo en canales marcados 18+)")
    @app_commands.describe(categoria="Categoría de imagen")
    @app_commands.choices(categoria=[
        app_commands.Choice(name=c, value=c) for c in CATEGORIAS
    ])
    async def nsfw(self, interaction: discord.Interaction, categoria: app_commands.Choice[str] = None):
        # Verificación obligatoria: el comando solo funciona en canales marcados como NSFW en Discord.
        if not isinstance(interaction.channel, discord.TextChannel) or not interaction.channel.is_nsfw():
            await interaction.response.send_message(
                "🔞 Este comando solo funciona en canales marcados como NSFW. "
                "Ve a la configuración del canal y actívalo primero.",
                ephemeral=True,
            )
            return

        cat = categoria.value if categoria else "waifu"
        await interaction.response.defer()
        url = await self.fetch_image(cat)

        if not url:
            await interaction.followup.send("❌ No pude traer una imagen ahorita, intenta de nuevo.")
            return

        embed = discord.Embed(color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_footer(text=f"Categoría: {cat}")
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(NSFW(bot))
