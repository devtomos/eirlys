from src.api.anilist.search import search, relations
from src.api.anilist.user import user
from src.api.general.errors import *
import asyncio


async def test_search():
    no_error_search = await search("Jujutsu Kaisen", "ANIME")
    print(no_error_search)
    await asyncio.sleep(2)
    try:
        force_error_search = await search("KEFJKLESJFLKESJKLFESJKLFJ", "ANIME")
    except StatusCodeError:
        print("status code was not 200")
    await asyncio.sleep(2)


async def test_user():
    no_error_user = await user("toemas")
    print(no_error_user)
    await asyncio.sleep(2)
    try:
        force_error_user = await user("WEALF;ERSKL;FGKERSL;GJKERTPDKLGJKLERDJGKL;ERJGL")
    except StatusCodeError:
        print("status code was not 200")
    await asyncio.sleep(2)


async def test_relations():
    no_error_relations = await relations("Jujutsu Kaisen", "ANIME")
    print(no_error_relations)
    await asyncio.sleep(2)
    try:
        force_error_relations = await relations("KEFJKLESJFLKESJKLFESJKLFJ", "ANIME")
    except StatusCodeError:
        print("status code was not 200")
    await asyncio.sleep(2)


async def run_funs():
    await test_search()
    await test_user()
    await test_relations()


asyncio.run(run_funs())
