import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Sincronizados {len(synced)} comandos slash.")
    except Exception as e:
        print(f"Error sincronizando comandos: {e}")


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"📦 Cog cargado: {filename}")


@bot.event
async def setup_hook():
    await load_cogs()


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("❌ No encontré DISCORD_TOKEN. Revisa tu archivo .env")
    bot.run(TOKEN)
