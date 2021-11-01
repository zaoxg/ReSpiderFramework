import asyncio


class AsyncBase:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.limit = 4
        pass

    async def next_task(self):
        semaphore = asyncio.Semaphore(value=self.limit)
        while True:
            try:
                task = self.fileList.pop()
                # print(task)
                await semaphore.acquire()
                self.loop.create_task(self.file_read(task, semaphore))
            except IndexError:
                print('Index Error')
                await asyncio.sleep(3)
                if len(asyncio.Task.all_tasks(loop=self.loop)) <= 1:
                    break
