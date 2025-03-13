import argparse
import asyncio
import aiopath
import aioshutil
import logging

# Парсимо вхідний командний рядок
parser = argparse.ArgumentParser(description="Sorting files")
parser.add_argument("--source", required=True, help="Source Dir")
parser.add_argument(
    "--destination", required=False, help="Destination dir", default="dst"
)
arguments = vars(parser.parse_args())

src_dir = aiopath.AsyncPath(arguments["source"])
dst_dir = aiopath.AsyncPath(arguments["destination"])


# Збираємо і віддаємо далі шляхи до всіх файлі з каталогу і підкаталогів
async def read_folder(path: aiopath.AsyncPath):
    async for file in path.iterdir():
        if await file.is_dir():
            await read_folder(file)
        else:
            await copy_file(file)


# Копіюємо файли згідно за їхнім розширенням до відповідних підкаталогів
async def copy_file(file: aiopath.AsyncPath):
    folder = dst_dir / file.suffix[1:]
    try:
        await folder.mkdir(parents=True, exist_ok=True)
        await aioshutil.copyfile(file, folder / file.name)
    except OSError as e:
        logging.error(e)


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    asyncio.run(read_folder(src_dir))
    print(
        f"Files has have been grouped and copied from '{src_dir}' to '{dst_dir}'."
    )
