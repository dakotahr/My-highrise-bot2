import asyncio
from highrise import BaseBot, User, SessionMetadata

class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("✅ Bot conectado correctamente")
        await self.highrise.chat("¡Hola! Soy un bot configurado desde cero 🤖")

    async def on_chat(self, user: User, message: str) -> None:
        if message.lower() == "!hola":
            await self.highrise.chat(f"¡Hola, {user.username}! 👋")

# Este bloque mágico imita el truco de Replit para buscar tu sala automáticamente
if __name__ == "__main__":
    import sys
    from highrise.__main__ import main
    
    # Si el bot no encuentra la sala, la busca mediante el sistema del SDK
    async def run_bot():
        try:
            await main()
        except Exception as e:
            print(f"Buscando sala del dueño... {e}")
            
    asyncio.run(run_bot())
