from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import typing as tp

import message_strings as msgstrings
from database import Database
from utils import parse_args, format_list, do_generate

F = tp.Callable[..., tp.Any]
bot = Bot(token=os.environ["BOT_TOKEN"], parse_mode="Markdown")
dp = Dispatcher(bot)
db = Database(os.environ["DB_URL"], os.environ["DB_TOKEN"])


def list_extractor(func: F) -> F:
    async def wrapper(message: types.Message) -> None:
        people_list = await db.get(message.chat.id)
        if not people_list:
            await message.reply(msgstrings.EMPTY_LIST)
            return
        await func(message, people_list)

    return wrapper


def command_with_two_positional_args(func: F) -> F:
    @dp.message_handler(commands=[func.__name__])
    @list_extractor
    async def wrapper(message: types.Message, people_list: tp.List[str]) -> None:
        from_idx, to_idx = parse_args(people_list, message.text)
        if from_idx < 0 or to_idx < 0 or from_idx >= len(people_list) or to_idx >= len(people_list):
            await message.reply(msgstrings.FORMAT_ERROR.format(command=func.__name__))
            return

        await func(people_list, from_idx, to_idx)
        await db.set(message.chat.id, people_list)
        await message.reply(msgstrings.MOVE_SUCCESS + format_list(people_list))

    return wrapper


@command_with_two_positional_args
async def move(people_list: tp.List[str], from_idx: int, to_idx: int) -> None:
    if from_idx < to_idx:
        to_idx += 1
    people_list.insert(to_idx, people_list[from_idx])
    if from_idx >= to_idx:
        from_idx += 1
    people_list.pop(from_idx)


@command_with_two_positional_args
async def swap(people_list: tp.List[str], from_idx: int, to_idx: int) -> None:
    people_list[from_idx], people_list[to_idx] = people_list[to_idx], people_list[from_idx]


@dp.message_handler(commands=["setlist"])
async def process_set_list(message: types.Message) -> None:
    people_list = message.text.split("\n")[1:]
    if len(people_list) == 0:
        await message.reply(msgstrings.LIST_CREATION_ERROR)
        return
    await db.set(message.chat.id, people_list)
    await message.reply(msgstrings.SAVE_SUCCESS)


@dp.message_handler(commands=["generate"])
@list_extractor
async def generate(message: types.Message, people_list: tp.List[str]) -> None:
    do_generate(people_list)
    await db.set(message.chat.id, people_list)
    await message.reply(msgstrings.GENERATE_SUCCESS + format_list(people_list))


@dp.message_handler(commands=["show"])
@list_extractor
async def show(message: types.Message, people_list: tp.List[str]) -> None:
    await message.reply(msgstrings.SHOW_SUCCESS + format_list(people_list))


@dp.message_handler(commands=["info", "start", "help"])
async def info(message: types.Message) -> None:
    await message.reply(msgstrings.INFORMATION)


if __name__ == "__main__":
    executor.start_polling(dp)
