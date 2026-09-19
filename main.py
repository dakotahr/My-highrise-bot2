import random
from highrise import BaseBot, User, SessionMetadata
from highrise.models import Position

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        # --- Variables de Control de Sistemas ---
        self.nombre_dueño = "IamDakota"  # ⚠️ ¡CAMBIA ESTO por tu nombre en Highrise sin el @!
        self.id_objetivo_seguir = None
        self.contador_visitas = 0
        self.contador_mensajes = 0
        
        # Coordenadas de la Zona VIP para el teletransporte grupal (Cámbialas si querés)
        self.vip_x = 5.5
        self.vip_y = 0.0
        self.vip_z = 5.5

        # Diccionario de emotes sencillos
        self.emotes_faciles = {
            "baile": "dance-shoppingcart", "baile2": "dance-tiktok8", "baile3": "dance-weird",
            "macarena": "dance-macarena", "beso": "emote-kiss", "flotar": "emote-float",
            "gravedad": "emote-gravity", "risa": "emote-laughing", "amor": "emote-lust",
            "saludo": "emote-curtsy", "llorar": "emote-cry", "susto": "emote-scared",
            "sueño": "emote-tired", "calor": "emote-hot"
        }
        
        # Frases inspiradoras y anuncios automáticos
        self.anuncios = [
            "📢 Recuerda dejar tu LIKE (❤️) a la sala para apoyarnos a seguir creciendo.",
            "📢 ¡Sigue al dueño de la sala para enterarte de futuros eventos y fiestas!",
            "✨ 'No cuentes los días, haz que los días cuenten.' - Muhammad Ali",
            "✨ 'La lógica te llevará desde A hasta B. La imaginación te llevará a todas partes.' - Albert Einstein",
            "✨ 'El único modo de hacer un gran trabajo es amar lo que haces.' - Steve Jobs",
            "📢 Si quieres divertirte, escribe !lista para ver mis emotes interactivos."
        ]

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("✅ Bot super avanzado conectado correctamente")
        posicion_inicial = Position(x=4.5, y=0.0, z=3.5, facing="FrontRight")
        await self.highrise.teleport(session_metadata.user_id, posicion_inicial)
        await self.highrise.chat("🤖 ¡Bot de Alta Tecnología Activo! Escribe !comandos para ver mis funciones.")

    # --- CONTADOR DE VISITAS Y BIENVENIDA ---
    async def on_user_join(self, user: User, position) -> None:
        self.contador_visitas += 1
        await self.highrise.chat(f"¡Bienvenido/a, {user.username}! 👋 Eres el visitante N° {self.contador_visitas} desde mi encendido. Escribe !lista")
        await self.highrise.send_emote("emote-curtsy")

    # --- SISTEMA INTELIGENTE PARA SEGUIR (Rastreador de movimiento) ---
    async def on_user_move(self, user: User, destination: Position) -> None:
        # Si el usuario que se acaba de mover es el objetivo asignado, el bot camina hacia él
        if self.id_objetivo_seguir and user.id == self.id_objetivo_seguir:
            try:
                # El bot camina a una posición cercana para no pisar al jugador
                nueva_pos = Position(x=destination.x - 0.5, y=destination.y, z=destination.z - 0.5, facing="FrontRight")
                await self.highrise.walk_to(nueva_pos)
            except Exception:
                pass

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.lower().strip()
        es_dueño = (user.username.lower() == self.nombre_dueño.lower())

        # --- CONTADOR DE MENSAJES Y ANUNCIOS AUTOMÁTICOS ---
        self.contador_mensajes += 1
        if self.contador_mensajes >= 20:
            self.contador_mensajes = 0
            frase_al_azar = random.choice(self.anuncios)
            await self.highrise.chat(frase_al_azar)

        # Muestra comandos básicos
        if msg == "!lista" or msg == "!comandos" or msg == "!emotes":
            await self.highrise.chat("✨ Di palabras comunes (baile, beso, flotar, risa) o escribe el nombre real de cualquier emote.")
            if es_dueño:
                await self.highrise.chat("👑 Comandos de dueño: !seguir | !quedarme | !vuelan todos | !visitas")
            return

        # --- COMANDOS EXCLUSIVOS DEL DUEÑO 👑 ---
        if msg == "!visitas" and es_dueño:
            await self.highrise.chat(f"📊 Registro actual: Hemos recibido {self.contador_visitas} visitas en esta sesión.")
            return

        if msg == "!vuelan todos" and es_dueño:
            await self.highrise.chat("🔮 ¡Poder del creador activo! Teletransportando a todos a la zona VIP...")
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
            await self.highrise.chat(f"🚶‍♂️ Entendido, mi creador. Iniciando protocolo de rastreo sobre ti.")
            return

        # Hacer que el bot siga a OTRA persona asignada por su nombre (Ej: !seguir juan)
        if msg.startswith("!seguir ") and es_dueño:
            nombre_objetivo = message[8:].strip().replace("@", "")
            room_users = await self.highrise.get_room_users()
            for room_user, position in room_users.content:
                if room_user.username.lower() == nombre_objetivo.lower():
                    self.id_objetivo_seguir = room_user.id
                    await self.highrise.chat(f"🚶‍♂️ Analizando objetivo... Fijando rastreo en @{room_user.username}.")
                    return
            await self.highrise.chat("❌ No encontré a ese usuario en la sala.")
            return

        if msg == "!quedarme" and es_dueño:
            self.id_objetivo_seguir = None
            await self.highrise.chat("🛑 Protocolo de rastreo desactivado. Me quedo en esta posición.")
            return

        # --- SISTEMA DE EMOTES SIMPLIFICADOS Y UNIVERSAL ---
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
