import requests
from typing import Dict
from src.api.anilist.queries import Query
from src.api.general.errors import *
from src.api.general.wide_functions import logger


async def user_search(username: str) -> Dict:
    """
        Search for user and return data related to them.

        :param username: str -- username for Anilist user.
    """

    response = requests.post(Query.url, json={'query': Query.user, 'variables': {'name': username}})
    request = response.json()
    data = request['data']['User']

    logger.info(f"Getting data for {username} from Anilist GraphQL API.")

    if response.status_code != 200:
        raise StatusCodeError(response.status_code, user_search.__name__)

    logger.info(f"Constructing user data for {username}")

    user_info = {
        'id': data['id'],
        'name': data['name'],
        'url': data['siteUrl'],
        'banner': data['bannerImage'],
        'avatar': data['avatar']['large'],
        'updated': data['updatedAt'],
        'animeCount': data['statistics']['anime']['count'],
        'animeMean': data['statistics']['anime']['meanScore'],
        'animeTime': data['statistics']['anime']['minutesWatched'],
        'animeWatch': data['statistics']['anime']['episodesWatched'],
        'mangaCount': data['statistics']['manga']['count'],
        'mangaMean': data['statistics']['manga']['meanScore'],
        'mangaChapter': data['statistics']['manga']['chaptersRead'],
        'mangaVolume': data['statistics']['manga']['volumesRead'],
        'errorCode': response.status_code}

    logger.info(f"Returning array with data from {username}")
    return user_info
