import random
import discord
from discord import app_commands
from discord.ext import commands


CHISTES = [
    "¿Por qué el programador se quedó sin batería? Porque no tenía cargador de humor.",
    "¿Cómo se llama un boomerang que no vuelve? Palo.",
    "Fui al médico y le dije: 'doctor, me duele todo el cuerpo al tocarlo'. Me dijo: 'deje de tocarse el cuerpo'.",
    "¿Qué le dice un jaguar a otro jaguar? Nada, los jaguares no hablan.",
    "Mi WiFi y mi vida amorosa tienen algo en común: ambos se desconectan solos.",
]

ROASTS = [
    "eres tan lento que el 5G te manda mensajes por carta.",
    "tienes menos personalidad que un formulario de Google.",
    "tu batería dura más que tu suerte con el WiFi.",
    "eres el 'ctrl+z' que nadie pidió.",
    "tienes el drip de una hoja de cálculo.",
]

FRASES_MOTIVACIONALES_FALSAS = [
    "El fracaso es solo el éxito en modo incógnito.",
    "No te rindas, ni siquiera tu router se rinde tan rápido reconectando.",
    "Cada gran programador alguna vez copió y pegó de Stack Overflow sin entender nada.",
]


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chiste", description="Te cuenta un chiste random")
    async def chiste(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(CHISTES))

    @app_commands.command(name="roast", description="Le tira un roast (broma pesada) a alguien")
    @app_commands.describe(usuario="A quién le tiras el roast")
    async def roast(self, interaction: discord.Interaction, usuario: discord.Member):
        if usuario.id == interaction.user.id:
            await interaction.response.send_message("¿Roasteándote a ti mismo? Ahí sí que estás mal 💀")
            return
        await interaction.response.send_message(f"{usuario.mention}, {random.choice(ROASTS)}")

    @app_commands.command(name="motivacion", description="Frase 'motivacional' random")
    async def motivacion(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"💪 {random.choice(FRASES_MOTIVACIONALES_FALSAS)}")

    @app_commands.command(name="moneda", description="Lanza una moneda")
    async def moneda(self, interaction: discord.Interaction):
        resultado = random.choice(["Cara", "Sello"])
        await interaction.response.send_message(f"🪙 Salió: **{resultado}**")

    @app_commands.command(name="8ball", description="Le preguntas algo a la bola 8")
    @app_commands.describe(pregunta="Tu pregunta para el oráculo")
    async def eightball(self, interaction: discord.Interaction, pregunta: str):
        respuestas = [
            "Sí, totalmente.", "No, ni de broma.", "Pregúntame más tarde.",
            "Muy probable.", "Lo dudo mucho.", "Es un sí seguro.",
            "Mejor no te digo.", "Las señales apuntan a que sí.",
        ]
        await interaction.response.send_message(f"🎱 Pregunta: *{pregunta}*\nRespuesta: **{random.choice(respuestas)}**")


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
