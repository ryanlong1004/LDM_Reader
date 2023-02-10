import asyncio
import sys


class LDMProtocol(asyncio.Protocol):
    def __init__(self, on_con_lost):
        self.transport = None
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print("Received:", data.decode())

    def connection_lost(self, exc):
        # The socket has been closed
        self.on_con_lost.set_result(True)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()
    transport, protocol = await loop.connect_read_pipe(
        lambda: LDMProtocol(on_con_lost), sys.stdin
    )

    try:
        await protocol.on_con_lost
    finally:
        transport.close()


asyncio.run(main())
