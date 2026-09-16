import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


class GuildMusicState:
    def __init__(self):
        self.queue = []  # lista de dicts {"title": str, "url": str}
        self.voice_client: discord.VoiceClient = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.states: dict[int, GuildMusicState] = {}

    def get_state(self, guild_id: int) -> GuildMusicState:
        if guild_id not in self.states:
            self.states[guild_id] = GuildMusicState()
        return self.states[guild_id]

    async def search(self, query: str):
        loop = asyncio.get_event_loop()

        def _extract():
            with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
                info = ydl.extract_info(query, download=False)
                if "entries" in info:
                    info = info["entries"][0]
                return info

        info = await loop.run_in_executor(None, _extract)
        return {"title": info.get("title", "Sin título"), "url": info["url"]}

    def play_next(self, guild: discord.Guild):
        state = self.get_state(guild.id)
        if not state.queue:
            return

        track = state.queue.pop(0)
        source = discord.FFmpegPCMAudio(track["url"], **FFMPEG_OPTS)

        def after_play(error):
            if error:
                print(f"Error reproduciendo: {error}")
            self.play_next(guild)

        state.voice_client.play(source, after=after_play)

    @app_commands.command(name="play", description="Reproduce una canción (nombre o link de YouTube)")
    @app_commands.describe(busqueda="Nombre de la canción o link")
    async def play(self, interaction: discord.Interaction, busqueda: str):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("❌ Tienes que estar en un canal de voz primero.", ephemeral=True)
            return

        await interaction.response.defer()
        state = self.get_state(interaction.guild.id)

        if state.voice_client is None or not state.voice_client.is_connected():
            state.voice_client = await interaction.user.voice.channel.connect()

        try:
            track = await self.search(busqueda)
        except Exception as e:
            await interaction.followup.send(f"❌ No pude encontrar eso: {e}")
            return

        state.queue.append(track)
        await interaction.followup.send(f"🎵 Agregado a la cola: **{track['title']}**")

        if not state.voice_client.is_playing() and not state.voice_client.is_paused():
            self.play_next(interaction.guild)

    @app_commands.command(name="skip", description="Salta la canción actual")
    async def skip(self, interaction: discord.Interaction):
        state = self.get_state(interaction.guild.id)
        if state.voice_client and state.voice_client.is_playing():
            state.voice_client.stop()
            await interaction.response.send_message("⏭️ Canción saltada.")
        else:
            await interaction.response.send_message("No hay nada sonando ahorita.", ephemeral=True)

    @app_commands.command(name="pause", description="Pausa la música")
    async def pause(self, interaction: discord.Interaction):
        state = self.get_state(interaction.guild.id)
        if state.voice_client and state.voice_client.is_playing():
            state.voice_client.pause()
            await interaction.response.send_message("⏸️ Pausado.")
        else:
            await interaction.response.send_message("No hay nada sonando.", ephemeral=True)

    @app_commands.command(name="resume", description="Reanuda la música")
    async def resume(self, interaction: discord.Interaction):
        state = self.get_state(interaction.guild.id)
        if state.voice_client and state.voice_client.is_paused():
            state.voice_client.resume()
            await interaction.response.send_message("▶️ Reanudado.")
        else:
            await interaction.response.send_message("No está pausado.", ephemeral=True)

    @app_commands.command(name="queue", description="Muestra la cola de reproducción")
    async def queue(self, interaction: discord.Interaction):
        state = self.get_state(interaction.guild.id)
        if not state.queue:
            await interaction.response.send_message("La cola está vacía.")
            return
        texto = "\n".join(f"{i+1}. {t['title']}" for i, t in enumerate(state.queue))
        await interaction.response.send_message(f"🎶 Cola:\n{texto}")

    @app_commands.command(name="stop", description="Detiene la música y saca al bot del canal de voz")
    async def stop(self, interaction: discord.Interaction):
        state = self.get_state(interaction.guild.id)
        state.queue.clear()
        if state.voice_client:
            await state.voice_client.disconnect()
            state.voice_client = None
        await interaction.response.send_message("⏹️ Detenido y desconectado.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
