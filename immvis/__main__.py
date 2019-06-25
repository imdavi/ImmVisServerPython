from immvis.server.immvisserver import start_server
from immvis.discovery.immvisdiscovery import start_service_discovery
import asyncio

if __name__ == '__main__':
    print("Running server...")
    loop = asyncio.get_event_loop()
    services = asyncio.gather(start_server(), start_service_discovery())
    loop.run_until_complete(services)
    loop.close()