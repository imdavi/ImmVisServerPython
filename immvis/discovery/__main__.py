import asyncio
from immvis.discovery.immvisdiscovery import start_service_discovery

loop = asyncio.get_event_loop()
loop.run_until_complete(start_service_discovery())
loop.close()