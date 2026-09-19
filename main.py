import random
import asyncio
from threading import Thread
from flask import Flask  # Servidor web invisible de fondo
from highrise import BaseBot, User, SessionMetadata
from highrise.models import Position

# --- SERVIDOR WEB INVISIBLE PARA EVITAR APAGONES ---
app = Flask('')

@app.route('/')
def home():
    return "¡Bot en línea 24/7!"

def run_web_server():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()

# --- CLASE PRINCIPAL DEL BOT ---
class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        # ⚠️ ¡Escribe tu nombre de usuario de Highrise sin el @ aquí abajo!
        self.nombre_dueño = "IamDakota"  
        self.id_objetivo_seguir = None
        self.contador_visitas = 0
        self.contador_mensajes = 0
        
        # Variables para el sistema de Trivia
        self.trivia_activa = False
        self.pregunta_actual = ""
        self.respuesta_correcta = ""
        
        self.vip_x = 5.5
        self.vip_y = 0.0
        self.vip_z = 5.5

        # Diccionario de emotes sencillos en español
        self.emotes_faciles = {
            "baile": "dance-shoppingcart", "baile2": "dance-tiktok8", "baile3": "dance-weird",
            "macarena": "dance-macarena", "beso": "emote-kiss", "flotar": "emote-float",
            "gravedad": "emote-gravity", "risa": "emote-laughing", "amor": "emote-lust",
            "saludo": "emote-curtsy", "llorar": "emote-cry", "susto": "emote-scared",
            "sueño": "emote-tired", "calor": "emote-hot"
        }
        
        # Base de datos de preguntas para la Trivia
        self.preguntas_trivia = [
            {"p": "¿Cuál es el planeta más cercano al Sol?", "r": "mercurio"},
            {"p": "¿Cuántos minutos tiene una hora?", "r": "60"},
            {"p": "¿Qué animal dice miau?", "r": "gato"},
            {"p": "¿Cuál es el color del cielo en un día despejado?", "r": "azul"},
            {"p": "¿Cuántos días tiene un año bisiesto?", "r": "366"}
        ]
        
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

        # --- RECONOCER RESPUESTAS DE LA TRIVIA ---
        if self.trivia_activa:
            if msg == self.respuesta_correcta:
                await self.highrise.chat(f"🎉 ¡CORRECTO, {user.username}! La respuesta era {self.respuesta_correcta.upper()}. Ganaste el juego.")
                await self.highrise.send_emote("dance-tiktok8", user.id)
                self.trivia_activa = False
                return

        # Contador de mensajes para anuncios masivos
        self.contador_mensajes += 1
        if self.contador_mensajes >= 5:  
            self.contador_mensajes = 0
            frase_al_azar = random.choice(self.anuncios)
            await self.highrise.chat(frase_al_azar)

        if msg == "!lista" or msg == "!comandos" or msg == "!emotes":
            await self.highrise.chat("✨ Di palabras comunes (baile, beso, flotar, risa) o el nombre de un emote.")
            await self.highrise.chat("🎮 Juego: Escribe !trivia para iniciar una pregunta.")
            if es_dueño:
                await self.highrise.chat("👑 Dueño: !seguir | !quedarme | !vuelan todos | !visitas | !clonar")
            return

        if msg == "!visitas" and es_dueño:
            await self.highrise.chat(f"📊 Registro actual: Hemos recibido {self.contador_visitas} visitas.")
            return

        # --- SISTEMA DE TRIVIA ---
        if msg == "!trivia":
            if self.trivia_activa:
                await self.highrise.chat(f"Ya hay una trivia en curso. La pregunta es: {self.pregunta_actual}")
            else:
                juego = random.choice(self.preguntas_trivia)
                self.pregunta_actual = juego["p"]
                self.respuesta_correcta = juego["r"]
                self.trivia_activa = True
                await self.highrise.chat("🧠 ¡COMIENZA LA TRIVIA! El primero en responder correctamente en el chat gana.")
                await self.highrise.chat(f"Pregunta: {self.pregunta_actual}")
            return

        # --- COMANDO CLONAR ROPA ---
        if msg == "!clonar" and es_dueño:
            await self.highrise.chat("🔍 Analizando tu outfit actual... Te pasaré los códigos por el chat:")
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, position in room_users.content:
                    if room_user.id == user.id:
                        outfit_data = await self.highrise.get_user_outfit(user.id)
                        for item in outfit_data.outfit:
                            await self.highrise.chat(f"Prenda tipo '{item.type}': ID -> {item.id}")
                        return
            except Exception as e:
                print(f"Error al escanear ropa: {e}")
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

        # Traductor de palabras fáciles
        for palabra_clave, nombre_real in self.emotes_faciles.items():
            if palabra_clave in msg:
                try:
                    await self.highrise.send_emote(nombre_real, user.id)
                    return
                except Exception:
                    pass

        # Intento de emote universal directo
        try:
            await self.highrise.send_emote(message.strip(), user.id)
        except Exception:
            pass

# --- INICIO DOBLE ---
if __name__ == "__main__":
    from highrise.__main__ import main as run_highrise
    
    keep_alive()  
    
    async def start():
        await run_highrise()
        
    asyncio.run(start())
