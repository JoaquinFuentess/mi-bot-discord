import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# ID de tu servidor, para que los comandos aparezcan al instante ahí
# (sin esto, los comandos globales pueden tardar hasta 1 hora en aparecer).
GUILD_ID = 659493071767207976
GUILD = discord.Object(id=GUILD_ID)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user} (ID: {bot.user.id})")
    try:
        # Sync global (tarda hasta 1 hora en propagarse a todos los servers)
        synced = await bot.tree.sync()
        print(f"🔄 Sincronizados {len(synced)} comandos slash (global).")

        # Sync directo a tu server (aparece al instante ahí)
        bot.tree.copy_global_to(guild=GUILD)
        synced_guild = await bot.tree.sync(guild=GUILD)
        print(f"⚡ Sincronizados {len(synced_guild)} comandos slash al instante en tu server.")
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
