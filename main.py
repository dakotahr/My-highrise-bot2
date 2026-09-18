from highrise import BaseBot, User, SessionMetadata

class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("✅ Bot conectado correctamente")
        await self.highrise.chat("¡Hola! Soy un bot configurado desde cero 🤖")

    async def on_chat(self, user: User, message: str) -> None:
        if message.lower() == "!hola":
            await self.highrise.chat(f"¡Hola, {user.username}! 👋")
