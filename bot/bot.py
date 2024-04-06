import asyncio
import sys


async def main(number=0):
    while True:
        print(number)
        number += 1
        await asyncio.sleep(1)

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    coro = main(int(sys.argv[1]) if len(sys.argv) > 1 else 0)

    event_loop.create_task(coro)
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
