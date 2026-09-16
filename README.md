# Mi Bot de Discord

Bot con comandos slash: diversión (`/chiste`, `/roast`, `/motivacion`, `/moneda`, `/8ball`), NSFW (`/nsfw`, solo funciona en canales marcados 18+) y música (`/play`, `/skip`, `/pause`, `/resume`, `/queue`, `/stop`).

## Música: instalar ffmpeg

Para que `/play` funcione necesitas `ffmpeg` instalado.

- **En tu PC (Linux)**: `sudo apt install ffmpeg`
- **En tu PC (Windows)**: descarga de https://ffmpeg.org/download.html y agrégalo al PATH
- **En Railway**: ya está resuelto, el archivo `nixpacks.toml` lo instala automático, no tienes que hacer nada.

## 1. Crear el bot en Discord

1. Ve a https://discord.com/developers/applications
2. Click en **New Application**, ponle el nombre que quieras (ese es el nombre público del bot).
3. En la pestaña **Bot**:
   - Click en **Reset Token** y copia el token (lo vas a necesitar después, NO lo compartas con nadie).
   - Activa **MESSAGE CONTENT INTENT** (abajo en "Privileged Gateway Intents").
   - Ahí mismo puedes subir la **foto de perfil** del bot.
4. En la pestaña **OAuth2 > URL Generator**:
   - Marca `bot` y `applications.commands`.
   - En permisos marca: Send Messages, Embed Links, Use Slash Commands.
   - Copia la URL generada abajo y ábrela en el navegador para invitar el bot a tu server.

## 2. Configurar el proyecto

Renombra `.env.example` a `.env` y pega tu token:

```
DISCORD_TOKEN=tu_token_aqui
```

## 3. Probarlo en tu PC (opcional)

```bash
pip install -r requirements.txt
python bot.py
```

## 4. Subirlo a Railway (para que corra 24/7)

1. Crea cuenta en https://railway.app (puedes entrar con GitHub).
2. Sube esta carpeta a un repo de GitHub (o usa "Deploy from GitHub repo" directo).
3. En Railway: **New Project > Deploy from GitHub repo**, elige el repo.
4. En **Variables**, agrega:
   - `DISCORD_TOKEN` = tu token
5. Railway va a detectar el `Procfile` y `nixpacks.toml`, instalar `ffmpeg` y correr el bot solo. Listo, ya está online 24/7.

## Notas

- El comando `/nsfw` solo va a responder en canales que tengas marcados como "Canal de edad restringida (NSFW)" en la configuración del canal de Discord. Esto es un requisito de Discord, no se puede saltar.
- Puedes agregar más comandos creando nuevos archivos en la carpeta `cogs/` siguiendo la misma estructura.
