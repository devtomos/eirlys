import nextcord, os, requests
from src.classes.defaultFuncs import *

anilistURL = 'https://graphql.anilist.co' #Default URL for Anilist
aniChecker = ['`Chapter          :` **None**\n', '`Volumes          :` **None**\n', '`All Episodes     :` **None**\n', '`Start Date       :` **None**\n', '`End Date         :` **None**\n', '`Popularity       :` **0**\n', '`Favourites       :` **0**\n', '`Genres           :` ****\n\n', '`Repeating        :`\n> ****\n\n', '`Completed        :`\n> ****\n\n', '`Current          :`\n> ****\n\n', '`Dropped          :`\n> ****\n\n', '`Planning         :`\n> ****\n\n']
affinityArray = {}

#[+] Anilist Queries [+]#
class Queries:

    search = '''
    query ($id: Int, $search: String, $type: MediaType) {
    Media (id: $id, search: $search, type: $type) {
            id
            season
            format
            episodes
            chapters
            volumes
            duration
            description
            status
            genres
            averageScore
            meanScore
            popularity
            siteUrl
            favourites
            bannerImage
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            airingSchedule(notYetAired: true){
                nodes{
                    timeUntilAiring
                    episode
                    }
            }
            relations{
                    nodes{
                        type
                        format
                        title{
                            romaji
                        }
                        siteUrl
                    }
                }
            characters(sort: ROLE){
                edges{
                    role
                    node{
                        name{
                            full
                        }
                        siteUrl
                    }
                }
            }
            studios(sort: NAME){
                nodes{
                    name
                }
            }
            rankings{
                rank
                context
                season
                year
            }
            startDate{
                year
                month
                day
            }
            endDate{
                year
                month
                day
            }
            coverImage{
                extraLarge
            }
            trailer{
                id
                site
            }
            title{
                romaji
                native
            }
        }
    }
    '''

# _________________________________________________________________________________________________________________________________________________________________ #

    relations = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        media (id: $id, search: $search) {
            id
            type
            title {
                romaji
                english
                native
                }
            }
        }
    }'''

# _________________________________________________________________________________________________________________________________________________________________ #

    userStatistics = '''
    query ($userName: String, $mediaId: Int) {
    MediaList(userName: $userName, mediaId: $mediaId) {
        progressVolumes
        status
        score(format: POINT_10)
        progress
        repeat
        }
    }
    '''

# _________________________________________________________________________________________________________________________________________________________________ #

    affinity = '''
        query ($userName: String, $perChunk: Int, $type: MediaType) {
        MediaListCollection (userName: $userName, perChunk: $perChunk, type: $type) {
            user {
                name
                avatar { large }
                siteUrl
            }
            lists {
                entries {
                status
                mediaId
                score(format: POINT_100)
            }}
            }
        }'''

# _________________________________________________________________________________________________________________________________________________________________ #

    user = '''
    query ($id: Int, $name: String) {
    User(id: $id, name: $name) {
        id
        name
        about
        siteUrl
        updatedAt
        bannerImage
        avatar {
            large
            medium
        }
        favourites{
            studios{
                nodes{
                    name
                }
            }
            staff{
                nodes{
                    name{
                        full
                        native
                    }
                }
            }
            characters{
                nodes{
                    name{
                        full
                        native
                        }
                    }
                }
            manga{
                nodes{
                    title{
                        romaji
                        native
                    }
                    type
                }
            }
            anime{
                nodes{
                    title{
                        romaji
                        native
                        }
                        type
                    }
                }
        }
        statistics {
            anime {
                count
                meanScore
                minutesWatched
                episodesWatched
                scores{
                    count
                    meanScore
                    score
                }
                formats {
                    count
                    format
                }
                statuses {
                    count
                    status
                }
                releaseYears {
                    count
                    releaseYear
                    }
                startYears {
                    count
                    startYear
                }
                genres {
                    count
                    genre
                    meanScore
                    minutesWatched
                }
            }
            manga {
                count
                meanScore
                standardDeviation
                chaptersRead
                volumesRead
                scores{
                    count
                    meanScore
                    score
                }
                formats {
                    count
                    format
                }
                statuses {
                    count
                    status
                }
                releaseYears {
                    count
                    releaseYear
                    }
                startYears {
                    count
                    startYear
                }
                genres {
                    count
                    genre
                    meanScore
                    minutesWatched
                }
                }
            }
        }
    }'''

# _________________________________________________________________________________________________________________________________________________________________ #

#[+] Anilist Functions [+]#
class Functions:

    #[+] Get Anime/Manga Close To What The User Said [+]#
    async def SearchRelations(searchName: str, type: str):
        relationID, relations, dups, amount = {}, [], [], 0
        response = requests.post(anilistURL, json={'query': Queries.relations, 'variables': {'search': searchName}})
        request = response.json()
        data = request['data']['Page']['media']

        # _________________________________________________________________________________________________________________________________________________________________ #

        clamp = len(data)-1
        totalClamp = max([clamp])
        while totalClamp >= 0:
            if clamp >= 0:
                if (searchName.split()[0].lower() in str(data[clamp]['title']['romaji']).lower()) or (str(data[clamp]['title']['english']).lower()) or (str(data[clamp]['title']['native']).lower()):
                    if data[clamp]['type'].upper() == type.upper():
                        if data[clamp]['title']['romaji'] in dups:
                            relations.append(nextcord.SelectOption(label=data[clamp]['title']['romaji'][:95] + f' | {amount}'))
                            relationID[data[clamp]['title']['romaji'][:95] + f' | {amount}'] = data[clamp]['id']
                            amount += 1
                        else:
                            dups.append(data[clamp]['title']['romaji'])
                            relations.append(nextcord.SelectOption(label=data[clamp]['title']['romaji'][:98]))
                            relationID[data[clamp]['title']['romaji'][:98]] = data[clamp]['id']
                clamp -= 1
            totalClamp -= 1

        # _________________________________________________________________________________________________________________________________________________________________ #

        if relations == []:
            relations.append(404)
        relations.reverse()

        return relationID, relations

# _________________________________________________________________________________________________________________________________________________________________ #

    #[+] Grab User Data For Specific Series [+]#
    async def userStats(username: str, seriesID: int):
        request = requests.post(anilistURL, json={'query': Queries.userStatistics, 'variables': {'userName': username, 'mediaId': seriesID}}); response = request.json()
        data = response['data']['MediaList']

        if data is None:
            data = {'progress': 0, 'status': 0, 'score': 0, 'progressVolumes': 0,'repeat': 0}
        else:
            data = {
                'progress': data['progress'], 'status': data['status'], 'score': data['score'], 'volume': data['progressVolumes'], 'repeat': data['repeat']}
        return data

# _________________________________________________________________________________________________________________________________________________________________ #

    #[+] Get Information On The Anime/Manga [+]#
    async def Search(searchName: str, members: list, id: bool, ty: str):
    
        if not id:
            var = {'search': searchName, 'type': ty}
        else:
            var = {'id': searchName, 'type': ty}
        
        response = requests.post(anilistURL, json={'query': Queries.search, 'variables': var})
        request = response.json()
        data = request['data']['Media']

        if response.status_code != 200:
            error = {'errorCode': response.status_code}; return error

        # _________________________________________________________________________________________________________________________________________________________________ #

        #[+] All Information Goes Here [+]#
        info = {
            'id': data['id'],
            'url': data['siteUrl'],
            'name': data['title']['romaji'],
            'avatar': data['coverImage']['extraLarge'],
            'banner': data['bannerImage'],
            'status': data['status'].capitalize(),
            'chapter': data['chapters'],
            'volumes': data['volumes'],
            'episodes': data['episodes'],
            'description': 'None',
            'startDate': f"{data['startDate']['day']}/{data['startDate']['month']}/{data['startDate']['year']}",
            'endDate': f"{data['endDate']['day']}/{data['endDate']['month']}/{data['endDate']['year']}",
            'popularity': data['popularity'],
            'avgScore': f"{data['averageScore']}%",
            'meanScore': f"{data['meanScore']}%",
            'genres': ', '.join(data['genres']),
            'favourites': data['favourites'],
            'repeating': [],
            'completed': [],
            'current': [],
            'dropped': [],
            'paused': [],
            'planning': [],
            'errorCode': response.status_code
            }

    # _________________________________________________________________________________________________________________________________________________________________ #

        #[+] Get User Scores If Members Is Not Empty [+]#
        if members != []:
            for member in members:
                uStats = await Functions.userStats(member, data['id'])

                if uStats['status'] == 'REPEATING':
                    info['repeating'].append(f"{member}: Current - {uStats['progress']} | {uStats['score']}/10")

                if uStats['status'] == 'COMPLETED':
                    if uStats['repeat'] != 0:
                        info['completed'].append(f"{member}: Repeats - {uStats['repeat']} | {uStats['score']}/10")
                    else:
                        info['completed'].append(f"{member}: {uStats['score']}/10")

                if uStats['status'] == 'CURRENT':
                    info['current'].append(f"{member}: Current - {uStats['progress']} | {uStats['score']}/10")

                if uStats['status'] == 'DROPPED':
                    info['dropped'].append(f"{member}: Last - {uStats['progress']}")

                if uStats['status'] == 'PAUSED':
                    info['paused'].append(f"{member}: Last - {uStats['progress']}")

                if uStats['status'] == 'PLANNING':
                    info['planning'].append(f"{member}")

    # _________________________________________________________________________________________________________________________________________________________________ #

        #[+] Alter Somethings Within The Dictionary [+]#
        if info['avatar'] == None:
            info['avatar'] = "https://i.imgur.com/FdFIkxG.png"

        if info['banner'] == None:
            info['banner'] = "https://i.imgur.com/FdFIkxG.png"

        if info['status'] == 'Not_yet_released':
            info['status'] = 'Not Yet Released'

        if info['avgScore'] == 'None%':
            info['avgScore'] = '0%'

        if info['meanScore'] == 'None%':
            info['meanScore'] = '0%'

        if info['endDate'].startswith('None'):
            info['endDate'] = 'None'
        
        if info['startDate'].startswith('None'):
            info['startDate'] = 'None'

    # _________________________________________________________________________________________________________________________________________________________________ #

        aniDes = [
            '`All Episodes     :` **{}**\n'.format(info['episodes']),
            '`Status           :` **{}**\n'.format(info['status']),
            '`Start Date       :` **{}**\n'.format(info['startDate']),
            '`End Date         :` **{}**\n'.format(info['endDate']),
            '`Avg Score        :` **{}**\n'.format(info['avgScore']),
            '`Mean Score       :` **{}**\n'.format(info['meanScore']),
            '`Popularity       :` **{:,}**\n'.format(info['popularity']),
            '`Favourites       :` **{}**\n'.format(info['favourites']),
            '`Genres           :` **{}**\n\n'.format(info['genres']),
            '`Repeating        :`\n> **{}**\n\n'.format('\n> '.join(info['repeating'])),
            '`Completed        :`\n> **{}**\n\n'.format('\n> '.join(info['completed'])),
            '`Current          :`\n> **{}**\n\n'.format('\n> '.join(info['current'])),
            '`Dropped          :`\n> **{}**\n\n'.format('\n> '.join(info['dropped']),
            '`Paused           :`\n> **{}**\n\n'.format('\n> '.join(info['paused']))),
            '`Planning         :`\n> **{}**\n\n'.format('\n> '.join(info['planning']))]

        for key, value in enumerate(aniDes):
            if value in aniChecker:
                aniDes[key] = ''

        return info, aniDes

# _________________________________________________________________________________________________________________________________________________________________ #

    #[+] Get Used Command Information [+]#
    async def FirstAni(usedComm: str):
        response = requests.post(anilistURL, json={'query': Queries.affinity, 'variables': {'userName': usedComm, 'perChunk': 500, 'type': 'ANIME'}}); request = response.json()
        data = request['data']['MediaListCollection']['lists']
        userInfo = request['data']['MediaListCollection']['user']

        affinityArray[usedComm] = {}
        affinityArray[usedComm]['ids'] = {}
        affinityArray[usedComm]['all'] = []

        dataClamp = len(data)-1
        totalClamp = max([dataClamp])
        while totalClamp >= 0:
            if dataClamp >= 0:
                lists = data[totalClamp]['entries']
                for entry in lists:
                    if entry['score'] == 0 or entry['status'] == 'PLANNING':
                        pass
                    else:
                        affinityArray[usedComm]['all'].append(entry['mediaId'])
                        affinityArray[usedComm]['ids'][entry["mediaId"]] = entry['score']
                dataClamp -= 1
            totalClamp -= 1

        userData = {'name': userInfo['name'], 'url': userInfo['siteUrl'], 'avatar': userInfo['avatar']['large']}
        return userData

    #[+] View The Affinity For All Within Guild [+]#
    async def Affinity(usedCommand: str, otherMember: str):
        response = requests.post(anilistURL, json={'query': Queries.affinity, 'variables': {'userName': otherMember, 'perChunk': 500, 'type': 'ANIME'}}); request = response.json()
        data = request['data']['MediaListCollection']['lists']
        userInfo = request['data']['MediaListCollection']['user']

        if otherMember == 'Last User In List':
            affinityArray.clear(); return

        if otherMember not in affinityArray:
            affinityArray[otherMember] = {}
            affinityArray[otherMember]['ids'] = {}
            affinityArray[otherMember]['all'] = []
            affinityArray[otherMember]['shares'] = []

        dataClamp = len(data)-1
        totalClamp = max([dataClamp])
        while totalClamp >= 0:
            if dataClamp >= 0:
                lists = data[totalClamp]['entries']
                for entry in lists:
                    if entry['score'] == 0 or entry['status'] == 'PLANNING':
                        pass
                    else:
                        affinityArray[otherMember]['all'].append(entry['mediaId'])
                        affinityArray[otherMember]['ids'][entry['mediaId']] = entry['score']
                dataClamp -= 1
            totalClamp -= 1

        for key in list(affinityArray[otherMember]['ids']):
            if key in affinityArray[usedCommand]['all']:
                affinityArray[otherMember]['ids'][key] = [affinityArray[usedCommand]['ids'][key], affinityArray[otherMember]['ids'][key]]
                affinityArray[otherMember]['shares'].append(key)
            else:
                del affinityArray[otherMember]['ids'][key]

        values = affinityArray[otherMember]['ids'].values()
        try: score1, score2 = list(zip(*values)); affinity = pearson(score1, score2)
        except: affinity = 0.0

        userDict = {'affinity': affinity, 'name': userInfo['name'], 'url': userInfo['siteUrl'], 'shares': len(affinityArray[otherMember]['shares'])}
        del affinityArray[otherMember]
        return userDict
        
# _________________________________________________________________________________________________________________________________________________________________ #

    #[+] View User Information [+]#
    async def User(username: str):
        response = requests.post(anilistURL, json={'query': Queries.user, 'variables': {'name': username}})
        request = response.json()
        data = request['data']['User']

        if response.status_code != 200:
            userInfo = {'errorCode': response.status_code}; return userInfo

        userInfo = {
            'id': data['id'],
            'name': data['name'],
            'about': data['about'],
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
            'mangaChapt': data['statistics']['manga']['chaptersRead'],
            'mangaVolume': data['statistics']['manga']['volumesRead'],
            'errorCode': response.status_code,}

        if userInfo['avatar'] == None:
            userInfo['avatar'] = "https://i.imgur.com/FdFIkxG.png"

        if userInfo['banner'] == None:
            userInfo['banner'] = "https://i.imgur.com/FdFIkxG.png"

        return userInfo

# _________________________________________________________________________________________________________________________________________________________________ #

    #[+] View Staff Information [+]#
    async def Staff(staffName: str):
        pass

# _________________________________________________________________________________________________________________________________________________________________ #

#[+] Anilist, Discord Commands [+]#
class TypeViewer(nextcord.ui.View):
    def __init__(self, options, optionsID, members, type):
        super().__init__()
        self.ops = options
        self.ids = optionsID
        self.mem = members
        self.ty = type
        self.add_item(TypeSelect(self.ops[:24], self.ids, self.mem, self.ty))

#[+] Pick A Title And View Information About It [+]#
class TypeSelect(nextcord.ui.Select):
    def __init__(self, options, optionsID, members, type):
        self.ops = options
        self.ids = optionsID
        self.mem = members
        self.ty = type
        super().__init__(placeholder="Choose A Title..", min_values=1, max_values=1, options=self.ops)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if self.values[0] != '' or None:
            ani = await Functions.Search(self.ids[self.values[0]], self.mem, True, self.ty)
            embed = nextcord.Embed(title=ani[0]['name'], url=ani[0]['url'], description=''.join(ani[1]), colour=int(os.getenv("COL"), 16))
            embed.set_image(url=ani[0]['banner'])
            embed.set_thumbnail(url=ani[0]['avatar'])
            await interaction.edit(embed=embed)
