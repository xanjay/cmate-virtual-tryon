import asyncio

sum = 0
sub = 0

async def add():
    print("Addition")
    await asyncio.sleep(4)
    return 5

async def subtract():
    print("Subtraction")
    await asyncio.sleep(4)
    return 4

loop = asyncio.get_event_loop()
sum, sub = loop.run_until_complete(asyncio.gather(
    add(),subtract()
))
loop.close()
print(sum,sub)