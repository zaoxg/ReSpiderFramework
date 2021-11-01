import asyncio
import csv
import aiofiles
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter


async def main():
    # simple reading
    async with aiofiles.open("some_file.csv", mode="r", encoding="utf-8", newline="") as afp:
        async for row in AsyncReader(afp):
            print(row)  # row is a list

    # dict reading, tab-separated
    async with aiofiles.open("some_other_file.tsv", mode="r", encoding="utf-8", newline="") as afp:
        async for row in AsyncDictReader(afp, delimiter="\t"):
            print(row)  # row is a dict


    # simple writing, "unix"-dialect
    async with aiofiles.open("new_file.csv", mode="w", encoding="utf-8", newline="") as afp:
        writer = AsyncWriter(afp, dialect="unix")
        await writer.writerow(["name", "age"])
        await writer.writerows([
            ["John", 26], ["Sasha", 42], ["Hana", 37]
        ])

    # dict writing, all quoted, "NULL" for missing fields
    async with aiofiles.open("new_file2.csv", mode="w", encoding="utf-8", newline="") as afp:
        writer = AsyncDictWriter(afp, ["name", "age"], restval="NULL", quoting=csv.QUOTE_ALL)
        await writer.writeheader()
        await writer.writerow({"name": "John", "age": 26})
        await writer.writerows([
            {"name": "Sasha", "age": 42},
            {"name": "Hana"}
        ])

# asyncio.run(main())

