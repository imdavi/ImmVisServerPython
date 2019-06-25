import asyncio
from immvis.server.immvisserver import start_server

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server())
loop.close()