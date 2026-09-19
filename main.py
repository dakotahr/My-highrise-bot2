from highrise import BaseBot, User, SessionMetadata

class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("✅ Bot conectado correctamente")
        await self.highrise.chat("¡Hola! Volví renovado y listo para bailar 🤖💃")

    async def on_chat(self, user: User, message: str) -> None:
        # Pasamos el mensaje a minúsculas para que no importen las mayúsculas
        msg = message.lower().strip()

        # --- COMANDO 1: Hacer bailar al bot ---
        if msg == "!dance":
            await self.highrise.chat(f"¡A mover el esqueleto, {user.username}! 🕺")
            # El bot ejecuta el emote de baile "dance-shoppingcart" sobre sí mismo
            await self.highrise.send_emote("dance-shoppingcart")

        # --- COMANDO 2: Lanzar un beso ---
        elif msg == "!beso":
            await self.highrise.send_emote("emote-kiss")

        # --- COMANDO 3: Hacer bailar a TODA la sala ---
        elif msg == "!bailartodos":
            await self.highrise.chat("¡Toda la sala a bailar! 🎉🥳")
            
            # Buscamos a todas las personas que están en la sala en este momento
            room_users = await self.highrise.get_room_users()
            
            # Recorremos la lista y le enviamos el emote a cada uno
            for room_user, position in room_users.content:
                try:
                    await self.highrise.send_emote("dance-tiktok8", room_user.id)
                except Exception:
                    # Si alguien está cargando o da error, el bot continúa con el siguiente
                    continue
