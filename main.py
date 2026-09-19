import random
from highrise import BaseBot, User, SessionMetadata

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.trivia_activa = False
        self.pregunta_actual = ""
        self.respuesta_correcta = ""
        
        # 🌟 DICCIONARIO DE PALABRAS CORTAS EN ESPAÑOL 🌟
        # A la izquierda pones cómo lo escribe el usuario, a la derecha el nombre técnico real del juego.
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
        await self.highrise.chat("¡Hola! Sistema simplificado activado. Solo di palabras como: baile, beso, flotar, risa... 🤖🎉")

    async def on_user_join(self, user: User, position) -> None:
        await self.highrise.chat(f"¡Bienvenido/a, {user.username}! 👋 Para bailar solo di la palabra: baile (o escribe !lista)")
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

        # Comando para ver la lista de palabras fáciles
        if msg == "!lista" or msg == "!comandos" or msg == "!emotes":
            await self.highrise.chat("✨ Di cualquiera de estas palabras en el chat para hacer el emote:")
            await self.highrise.chat("baile | baile2 | baile3 | macarena | beso | flotar | gravedad")
            await self.highrise.chat("risa | amor | saludo | llorar | susto | sueño | calor")
            return

        # Comando masivo
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

        # --- 🌟 DETECTOR INTELIGENTE DE PALABRAS EN ESPAÑOL 🌟 ---
        # Recorre la lista de palabras fáciles. Si el mensaje contiene esa palabra, tira el emote.
        for palabra_clave, nombre_real in self.emotes_faciles.items():
            if palabra_clave in msg:
                try:
                    await self.highrise.send_emote(nombre_real, user.id)
                    return  # Frena el código para que no intente buscar más palabras en el mismo mensaje
                except Exception:
                    print(f"Error al ejecutar: {nombre_real}")

