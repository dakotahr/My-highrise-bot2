import random
from highrise import BaseBot, User, SessionMetadata
from highrise.models import Position  # Importamos esto para mover al bot

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.trivia_activa = False
        self.pregunta_actual = ""
        self.respuesta_correcta = ""
        
        # Diccionario de apodos fáciles en español
        self.emotes_faciles = {
            "baile": "dance-shoppingcart",
            "baile2": "dance-tiktok8",
            "baile3": "dance-weird",
            "macarena": "dance-macarena",
            "beso": "emote-kiss",
            "flotar": "emote-float",
            "gravedad": "emote-gravity",
            "risa": "emote-laughing",
            "amor": "emote-lust",
            "saludo": "emote-curtsy",
            "llorar": "emote-cry",
            "susto": "emote-scared",
            "sueño": "emote-tired",
            "calor": "emote-hot"
        }
        
        self.preguntas_trivia = [
            {"p": "¿Cuál es el planeta más cercano al Sol?", "r": "mercurio"},
            {"p": "¿Cuántos minutos tiene una hora?", "r": "60"},
            {"p": "¿Qué animal dice miau?", "r": "gato"},
            {"p": "¿Cuál es el color del cielo en un día despejado?", "r": "azul"},
            {"p": "¿Cuántos días tiene un año bisiesto?", "r": "366"}
        ]

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("✅ Bot conectado correctamente")
        
        # 📍 CONFIGURACIÓN DE POSICIÓN 📍
        # Cambiá estos números (X, Y, Z) para ubicar al bot donde quieras en tu sala:
        # X = Horizontal, Y = Altura/Piso, Z = Profundidad, facing = Hacia dónde mira (FrontRight, FrontLeft, etc.)
        posicion_bot = Position(x=4.5, y=0.0, z=3.5, facing="FrontRight")
        
        # Le ordenamos al bot teletransportarse a ese lugar exacto apenas entra
        await self.highrise.teleport(session_metadata.user_id, posicion_bot)
        await self.highrise.chat("¡Hola! Estoy listo en mi puesto. Decí cualquier emote del juego o palabras fáciles 🤖🎉")

    async def on_user_join(self, user: User, position) -> None:
        await self.highrise.chat(f"¡Bienvenido/a, {user.username}! 👋 Escribe !lista para ver los emotes rápidos.")
        await self.highrise.send_emote("emote-curtsy")

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.lower().strip()

        # Control de la Trivia
        if self.trivia_activa:
            if msg == self.respuesta_correcta:
                await self.highrise.chat(f"🎉 ¡CORRECTO, {user.username}! La respuesta era {self.respuesta_correcta.upper()}. Ganaste.")
                await self.highrise.send_emote("dance-tiktok8", user.id)
                self.trivia_activa = False
                return

        if msg == "!lista" or msg == "!comandos" or msg == "!emotes":
            await self.highrise.chat("✨ Podés decir palabras fáciles (baile, beso, flotar, risa) o escribir directamente el nombre real de CUALQUIER emote del juego (ej: cozynap)")
            return

        if msg == "!bailartodos":
            await self.highrise.chat("¡Toda la sala a bailar! 🎉🥳")
            room_users = await self.highrise.get_room_users()
            for room_user, position in room_users.content:
                try:
                    await self.highrise.send_emote("dance-tiktok8", room_user.id)
                except Exception:
                    continue
            return

        if msg == "!trivia":
            if self.trivia_activa:
                await self.highrise.chat(f"Ya hay una trivia en curso. La pregunta es: {self.pregunta_actual}")
            else:
                juego = random.choice(self.preguntas_trivia)
                self.pregunta_actual = juego["p"]
                self.respuesta_correcta = juego["r"]
                self.trivia_activa = True
                await self.highrise.chat("🧠 ¡COMIENZA LA TRIVIA! El primero en responder correctamente gana.")
                await self.highrise.chat(f"Pregunta: {self.pregunta_actual}")
            return

        # --- 🌟 1. BUSCADOR EN LA LISTA EN ESPAÑOL 🌟 ---
        for palabra_clave, nombre_real in self.emotes_faciles.items():
            if palabra_clave in msg:
                try:
                    await self.highrise.send_emote(nombre_real, user.id)
                    return
                except Exception:
                    pass

        # --- 🌟 2. SISTEMA UNIVERSAL (Cualquier emote del juego) 🌟 ---
        # Si el usuario no usó una palabra en español, el bot intenta interpretar el texto directo como un emote oficial
        try:
            # Intentamos enviarle el emote tal cual como lo escribió (ej: cozynap)
            await self.highrise.send_emote(message.strip(), user.id)
        except Exception:
            # Si el emote no existe en todo Highrise, el bot ignora el mensaje y no se traba
            pass
