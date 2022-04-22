import asyncio
import time

i = 0


async def say_after(delay, what):
    global i
    await asyncio.sleep(delay)
    if what == 'hello':
        i += 1
    print(what)

async def main():

    print(f"finished at {time.strftime('%X')}")
    string = {'hello': 1,
              'world': 2}
    tasks = []
    for _ in range(100):
        for key, val in string.items():
            asyncio.create_task(say_after(val, key))
            # tasks.append(asyncio.create_task(say_after(val, key)))
    # await asyncio.gather(*tasks)
    # loop.run_forever()

    print(f"finished at {time.strftime('%X')}")
    print(i)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())