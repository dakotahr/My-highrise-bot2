import random
import asyncio
from threading import Thread
from flask import Flask  # Servidor web invisible de fondo
from highrise import BaseBot, User, SessionMetadata
from highrise.models import Position

# --- SERVIDOR WEB INVISIBLE PARA EVITAR APAGONES ---
app = Flask('')

@app.route('/')
def home():
    return "¡Bot en línea 24/7!"

def run_web_server():
    # Render usa el puerto 10000 por defecto en Web Services
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()

# --- CLASE PRINCIPAL DEL BOT ---
class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.nombre_dueño = "IamDakota"  # ⚠️ ¡Escribe tu nombre de Highrise sin el @!
        self.id_objetivo_seguir = None
        self.contador_visitas = 0
        self.contador_mensajes = 0
        
        self.vip_x = 5.5
        self.vip_y = 0.0
        self.vip_z = 5.5

        self.emotes_faciles = {
            "baile": "dance-shoppingcart", "baile2": "dance-tiktok8", "baile3": "dance-weird",
            "macarena": "dance-macarena", "beso": "emote-kiss", "flotar": "emote-float",
            "gravedad": "emote-gravity", "risa": "emote-laughing", "amor": "emote-lust",
            "saludo": "emote-curtsy", "llorar": "emote-cry", "susto": "emote-scared",
            "sueño": "emote-tired", "calor": "emote-hot"
        }
        
        self.anuncios = [
            "📢 Recuerda dejar tu LIKE (❤️) a la sala para apoyarnos a seguir creciendo.",
            "📢 ¡Sigue al dueño de la sala para enterarte de futuros eventos y fiestas!",
            "✨ 'No cuentes los días, haz que los días cuenten.' - Muhammad Ali",
            "✨ 'El único modo de hacer un gran trabajo es amar lo que haces.' - Steve Jobs",
            "📢 Si quieres divertirte, escribe !lista para ver mis emotes interactivos."
        ]

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("✅ Bot super avanzado conectado correctamente")
        posicion_inicial = Position(x=4.5, y=0.0, z=3.5, facing="FrontRight")
        await self.highrise.teleport(session_metadata.user_id, posicion_inicial)
        await self.highrise.chat("🤖 ¡Bot de Alta Tecnología Activo! Escribe !comandos para ver mis funciones.")

    async def on_user_join(self, user: User, position) -> None:
        self.contador_visitas += 1
        await self.highrise.chat(f"¡Bienvenido/a, {user.username}! 👋 Eres el visitante N° {self.contador_visitas}. Escribe !lista")
        await self.highrise.send_emote("emote-curtsy")

    async def on_user_move(self, user: User, destination: Position) -> None:
        if self.id_objetivo_seguir and user.id == self.id_objetivo_seguir:
            try:
                nueva_pos = Position(x=destination.x - 0.5, y=destination.y, z=destination.z - 0.5, facing="FrontRight")
                await self.highrise.walk_to(nueva_pos)
            except Exception:
                pass

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.lower().strip()
        es_dueño = (user.username.lower() == self.nombre_dueño.lower())

        self.contador_mensajes += 1
        if self.contador_mensajes >= 5:  # Baje de 20 a 5 para que tire anuncios más rápido
            self.contador_mensajes = 0
            frase_al_azar = random.choice(self.anuncios)
            await self.highrise.chat(frase_al_azar)

        if msg == "!lista" or msg == "!comandos" or msg == "!emotes":
            await self.highrise.chat("✨ Di palabras comunes (baile, beso, flotar, risa) o el nombre técnico de un emote.")
            if es_dueño:
                await self.highrise.chat("👑 Dueño: !seguir | !quedarme | !vuelan todos | !visitas")
            return

        if msg == "!visitas" and es_dueño:
            await self.highrise.chat(f"📊 Registro actual: Hemos recibido {self.contador_visitas} visitas.")
            return

        if msg == "!vuelan todos" and es_dueño:
            await self.highrise.chat("🔮 ¡Teletransportando a todos a la zona VIP...")
            room_users = await self.highrise.get_room_users()
            for room_user, position in room_users.content:
                try:
                    dest_vip = Position(x=self.vip_x, y=self.vip_y, z=self.vip_z, facing="FrontRight")
                    await self.highrise.teleport(room_user.id, dest_vip)
                except Exception:
                    continue
            return

        if msg == "!seguir" and es_dueño:
            self.id_objetivo_seguir = user.id
            await self.highrise.chat(f"🚶‍♂️ Protocolo de rastreo fijado en ti, mi creador.")
            return

        if msg.startswith("!seguir ") and es_dueño:
            nombre_objetivo = message[8:].strip().replace("@", "")
            room_users = await self.highrise.get_room_users()
            for room_user, position in room_users.content:
                if room_user.username.lower() == nombre_objetivo.lower():
                    self.id_objetivo_seguir = room_user.id
                    await self.highrise.chat(f"🚶‍♂️ Buscando... Rastreo fijado en @{room_user.username}.")
                    return
            await self.highrise.chat("❌ No encontré a ese usuario en la sala.")
            return

        if msg == "!quedarme" and es_dueño:
            self.id_objetivo_seguir = None
            await self.highrise.chat("🛑 Me quedo en esta posición.")
            return

        for palabra_clave, nombre_real in self.emotes_faciles.items():
            if palabra_clave in msg:
                try:
                    await self.highrise.send_emote(nombre_real, user.id)
                    return
                except Exception:
                    pass

        try:
            await self.highrise.send_emote(message.strip(), user.id)
        except Exception:
            pass

# --- INICIO DOBLE (Arranca el servidor web y luego el bot de juego) ---
if __name__ == "__main__":
    import sys
    from highrise.__main__ import main as run_highrise
    
    # Encendemos la señal de vida para UptimeRobot
    keep_alive()
    
    # Dejamos que Highrise tome el control del bucle principal
    async def start():
        await run_highrise()
        
    asyncio.run(start())
