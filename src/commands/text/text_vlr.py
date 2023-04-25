import nextcord
from nextcord.ext import commands
from src.api.general.wide_functions import *
from src.api.vlr.upcoming import match
from src.api.general.wide_components import VLRPage

class TextVLR(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def match(self, ctx, url):
        game = await match(url)
        all_stat_list = [
            '`{:^21}`'.format('Game Info'),
            '`{:<8}:` `{:^5}:{:^5}`'.format('Score', game['team_1_score'], game['team_2_score']),
            '`{:<8}:` `{:^11}`'.format('Page', 'All Stats') + '\n',


            f"**{game['all_stats']['team_1']['team_name']}**",
            "`{:<8}:` `{:^5}` `{:^17}` `{:^5}` `{:^5}`".format('Name', 'ACS', 'K/D/A', 'ADR', 'HS%'),
            f"`{game['all_stats']['team_1']['player_1']['name'][:8]:<8}:` `{game['all_stats']['team_1']['player_1']['acs']:^5}` `{game['all_stats']['team_1']['player_1']['kills']:^5}/{game['all_stats']['team_1']['player_1']['deaths']:^5}/{game['all_stats']['team_1']['player_1']['assists']:^5}` `{game['all_stats']['team_1']['player_1']['adr']:^5}` `{game['all_stats']['team_1']['player_1']['hs']:^5}`",
            f"`{game['all_stats']['team_1']['player_2']['name'][:8]:<8}:` `{game['all_stats']['team_1']['player_2']['acs']:^5}` `{game['all_stats']['team_1']['player_2']['kills']:^5}/{game['all_stats']['team_1']['player_2']['deaths']:^5}/{game['all_stats']['team_1']['player_2']['assists']:^5}` `{game['all_stats']['team_1']['player_2']['adr']:^5}` `{game['all_stats']['team_1']['player_2']['hs']:^5}`",
            f"`{game['all_stats']['team_1']['player_3']['name'][:8]:<8}:` `{game['all_stats']['team_1']['player_3']['acs']:^5}` `{game['all_stats']['team_1']['player_3']['kills']:^5}/{game['all_stats']['team_1']['player_3']['deaths']:^5}/{game['all_stats']['team_1']['player_3']['assists']:^5}` `{game['all_stats']['team_1']['player_3']['adr']:^5}` `{game['all_stats']['team_1']['player_3']['hs']:^5}`",
            f"`{game['all_stats']['team_1']['player_4']['name'][:8]:<8}:` `{game['all_stats']['team_1']['player_4']['acs']:^5}` `{game['all_stats']['team_1']['player_4']['kills']:^5}/{game['all_stats']['team_1']['player_4']['deaths']:^5}/{game['all_stats']['team_1']['player_4']['assists']:^5}` `{game['all_stats']['team_1']['player_4']['adr']:^5}` `{game['all_stats']['team_1']['player_4']['hs']:^5}`",
            f"`{game['all_stats']['team_1']['player_5']['name'][:8]:<8}:` `{game['all_stats']['team_1']['player_5']['acs']:^5}` `{game['all_stats']['team_1']['player_5']['kills']:^5}/{game['all_stats']['team_1']['player_5']['deaths']:^5}/{game['all_stats']['team_1']['player_5']['assists']:^5}` `{game['all_stats']['team_1']['player_5']['adr']:^5}` `{game['all_stats']['team_1']['player_5']['hs']:^5}`\n\n",

            f"**{game['all_stats']['team_2']['team_name']}**",
            "`{:<8}:` `{:^5}` `{:^17}` `{:^5}` `{:^5}`".format('Name', 'ACS', 'K/D/A', 'ADR', 'HS%'),
            f"`{game['all_stats']['team_2']['player_1']['name'][:8]:<8}:` `{game['all_stats']['team_2']['player_1']['acs']:^5}` `{game['all_stats']['team_2']['player_1']['kills']:^5}/{game['all_stats']['team_2']['player_1']['deaths']:^5}/{game['all_stats']['team_2']['player_1']['assists']:^5}` `{game['all_stats']['team_2']['player_1']['adr']:^5}` `{game['all_stats']['team_2']['player_1']['hs']:^5}`",
            f"`{game['all_stats']['team_2']['player_2']['name'][:8]:<8}:` `{game['all_stats']['team_2']['player_2']['acs']:^5}` `{game['all_stats']['team_2']['player_2']['kills']:^5}/{game['all_stats']['team_2']['player_2']['deaths']:^5}/{game['all_stats']['team_2']['player_2']['assists']:^5}` `{game['all_stats']['team_2']['player_2']['adr']:^5}` `{game['all_stats']['team_2']['player_2']['hs']:^5}`",
            f"`{game['all_stats']['team_2']['player_3']['name'][:8]:<8}:` `{game['all_stats']['team_2']['player_3']['acs']:^5}` `{game['all_stats']['team_2']['player_3']['kills']:^5}/{game['all_stats']['team_2']['player_3']['deaths']:^5}/{game['all_stats']['team_2']['player_3']['assists']:^5}` `{game['all_stats']['team_2']['player_3']['adr']:^5}` `{game['all_stats']['team_2']['player_3']['hs']:^5}`",
            f"`{game['all_stats']['team_2']['player_4']['name'][:8]:<8}:` `{game['all_stats']['team_2']['player_4']['acs']:^5}` `{game['all_stats']['team_2']['player_4']['kills']:^5}/{game['all_stats']['team_2']['player_4']['deaths']:^5}/{game['all_stats']['team_2']['player_4']['assists']:^5}` `{game['all_stats']['team_2']['player_4']['adr']:^5}` `{game['all_stats']['team_2']['player_4']['hs']:^5}`",
            f"`{game['all_stats']['team_2']['player_5']['name'][:8]:<8}:` `{game['all_stats']['team_2']['player_5']['acs']:^5}` `{game['all_stats']['team_2']['player_5']['kills']:^5}/{game['all_stats']['team_2']['player_5']['deaths']:^5}/{game['all_stats']['team_2']['player_5']['assists']:^5}` `{game['all_stats']['team_2']['player_5']['adr']:^5}` `{game['all_stats']['team_2']['player_5']['hs']:^5}`",
            ]
        map_one_list =  [
            '`{:^21}`'.format('Game Info'),
            '`{:<8}:` `{:^5}:{:^5}`'.format('F-Score', game['team_1_score'], game['team_2_score']),
            '`{:<8}:` `{:^5}:{:^5}`'.format('M-Score', game['map_one']['team_1_score'], game['map_one']['team_2_score']),
            '`{:<8}:` `{:^11}`'.format('Map Pick', game['map_one']['map_name']),
            '`{:<8}:` `{:^11}`'.format('Duration', game['map_one']['map_duration']),
            '`{:<8}:` `{:^11}`'.format('Page', 'Match One') + '\n',


            f"**{game['map_one']['team_1']['team_name']}**",
            "`{:<8}:` `{:^5}` `{:^17}` `{:^5}` `{:^5}`".format('Name', 'ACS', 'K/D/A', 'ADR', 'HS%'),
            f"`{game['map_one']['team_1']['player_1']['name'][:8]:<8}:` `{game['map_one']['team_1']['player_1']['acs']:^5}` `{game['map_one']['team_1']['player_1']['kills']:^5}/{game['map_one']['team_1']['player_1']['deaths']:^5}/{game['map_one']['team_1']['player_1']['assists']:^5}` `{game['map_one']['team_1']['player_1']['adr']:^5}` `{game['map_one']['team_1']['player_1']['hs']:^5}`",
            f"`{game['map_one']['team_1']['player_2']['name'][:8]:<8}:` `{game['map_one']['team_1']['player_2']['acs']:^5}` `{game['map_one']['team_1']['player_2']['kills']:^5}/{game['map_one']['team_1']['player_2']['deaths']:^5}/{game['map_one']['team_1']['player_2']['assists']:^5}` `{game['map_one']['team_1']['player_2']['adr']:^5}` `{game['map_one']['team_1']['player_2']['hs']:^5}`",
            f"`{game['map_one']['team_1']['player_3']['name'][:8]:<8}:` `{game['map_one']['team_1']['player_3']['acs']:^5}` `{game['map_one']['team_1']['player_3']['kills']:^5}/{game['map_one']['team_1']['player_3']['deaths']:^5}/{game['map_one']['team_1']['player_3']['assists']:^5}` `{game['map_one']['team_1']['player_3']['adr']:^5}` `{game['map_one']['team_1']['player_3']['hs']:^5}`",
            f"`{game['map_one']['team_1']['player_4']['name'][:8]:<8}:` `{game['map_one']['team_1']['player_4']['acs']:^5}` `{game['map_one']['team_1']['player_4']['kills']:^5}/{game['map_one']['team_1']['player_4']['deaths']:^5}/{game['map_one']['team_1']['player_4']['assists']:^5}` `{game['map_one']['team_1']['player_4']['adr']:^5}` `{game['map_one']['team_1']['player_4']['hs']:^5}`",
            f"`{game['map_one']['team_1']['player_5']['name'][:8]:<8}:` `{game['map_one']['team_1']['player_5']['acs']:^5}` `{game['map_one']['team_1']['player_5']['kills']:^5}/{game['map_one']['team_1']['player_5']['deaths']:^5}/{game['map_one']['team_1']['player_5']['assists']:^5}` `{game['map_one']['team_1']['player_5']['adr']:^5}` `{game['map_one']['team_1']['player_5']['hs']:^5}`\n\n",

            f"**{game['map_one']['team_2']['team_name']}**",
            "`{:<8}:` `{:^5}` `{:^17}` `{:^5}` `{:^5}`".format('Name', 'ACS', 'K/D/A', 'ADR', 'HS%'),
            f"`{game['map_one']['team_2']['player_1']['name'][:8]:<8}:` `{game['map_one']['team_2']['player_1']['acs']:^5}` `{game['map_one']['team_2']['player_1']['kills']:^5}/{game['map_one']['team_2']['player_1']['deaths']:^5}/{game['map_one']['team_2']['player_1']['assists']:^5}` `{game['map_one']['team_2']['player_1']['adr']:^5}` `{game['map_one']['team_2']['player_1']['hs']:^5}`",
            f"`{game['map_one']['team_2']['player_2']['name'][:8]:<8}:` `{game['map_one']['team_2']['player_2']['acs']:^5}` `{game['map_one']['team_2']['player_2']['kills']:^5}/{game['map_one']['team_2']['player_2']['deaths']:^5}/{game['map_one']['team_2']['player_2']['assists']:^5}` `{game['map_one']['team_2']['player_2']['adr']:^5}` `{game['map_one']['team_2']['player_2']['hs']:^5}`",
            f"`{game['map_one']['team_2']['player_3']['name'][:8]:<8}:` `{game['map_one']['team_2']['player_3']['acs']:^5}` `{game['map_one']['team_2']['player_3']['kills']:^5}/{game['map_one']['team_2']['player_3']['deaths']:^5}/{game['map_one']['team_2']['player_3']['assists']:^5}` `{game['map_one']['team_2']['player_3']['adr']:^5}` `{game['map_one']['team_2']['player_3']['hs']:^5}`",
            f"`{game['map_one']['team_2']['player_4']['name'][:8]:<8}:` `{game['map_one']['team_2']['player_4']['acs']:^5}` `{game['map_one']['team_2']['player_4']['kills']:^5}/{game['map_one']['team_2']['player_4']['deaths']:^5}/{game['map_one']['team_2']['player_4']['assists']:^5}` `{game['map_one']['team_2']['player_4']['adr']:^5}` `{game['map_one']['team_2']['player_4']['hs']:^5}`",
            f"`{game['map_one']['team_2']['player_5']['name'][:8]:<8}:` `{game['map_one']['team_2']['player_5']['acs']:^5}` `{game['map_one']['team_2']['player_5']['kills']:^5}/{game['map_one']['team_2']['player_5']['deaths']:^5}/{game['map_one']['team_2']['player_5']['assists']:^5}` `{game['map_one']['team_2']['player_5']['adr']:^5}` `{game['map_one']['team_2']['player_5']['hs']:^5}`",
            ]                    
        map_two_list = [
            '`{:^21}`'.format('Game Info'),
            '`{:<8}:` `{:^5}:{:^5}`'.format('F-Score', game['team_1_score'], game['team_2_score']),
            '`{:<8}:` `{:^5}:{:^5}`'.format('M-Score', game['map_two']['team_1_score'], game['map_two']['team_2_score']),
            '`{:<8}:` `{:^11}`'.format('Map Pick', game['map_two']['map_name']),
            '`{:<8}:` `{:^11}`'.format('Duration', game['map_two']['map_duration']),
            '`{:<8}:` `{:^11}`'.format('Page', 'Match Two') + '\n',


            f"**{game['map_two']['team_1']['team_name']}**",
            "`{:<8}:` `{:^5}` `{:^17}` `{:^5}` `{:^5}`".format('Name', 'ACS', 'K/D/A', 'ADR', 'HS%'),
            f"`{game['map_two']['team_1']['player_1']['name'][:8]:<8}:` `{game['map_two']['team_1']['player_1']['acs']:^5}` `{game['map_two']['team_1']['player_1']['kills']:^5}/{game['map_two']['team_1']['player_1']['deaths']:^5}/{game['map_two']['team_1']['player_1']['assists']:^5}` `{game['map_two']['team_1']['player_1']['adr']:^5}` `{game['map_two']['team_1']['player_1']['hs']:^5}`",
            f"`{game['map_two']['team_1']['player_2']['name'][:8]:<8}:` `{game['map_two']['team_1']['player_2']['acs']:^5}` `{game['map_two']['team_1']['player_2']['kills']:^5}/{game['map_two']['team_1']['player_2']['deaths']:^5}/{game['map_two']['team_1']['player_2']['assists']:^5}` `{game['map_two']['team_1']['player_2']['adr']:^5}` `{game['map_two']['team_1']['player_2']['hs']:^5}`",
            f"`{game['map_two']['team_1']['player_3']['name'][:8]:<8}:` `{game['map_two']['team_1']['player_3']['acs']:^5}` `{game['map_two']['team_1']['player_3']['kills']:^5}/{game['map_two']['team_1']['player_3']['deaths']:^5}/{game['map_two']['team_1']['player_3']['assists']:^5}` `{game['map_two']['team_1']['player_3']['adr']:^5}` `{game['map_two']['team_1']['player_3']['hs']:^5}`",
            f"`{game['map_two']['team_1']['player_4']['name'][:8]:<8}:` `{game['map_two']['team_1']['player_4']['acs']:^5}` `{game['map_two']['team_1']['player_4']['kills']:^5}/{game['map_two']['team_1']['player_4']['deaths']:^5}/{game['map_two']['team_1']['player_4']['assists']:^5}` `{game['map_two']['team_1']['player_4']['adr']:^5}` `{game['map_two']['team_1']['player_4']['hs']:^5}`",
            f"`{game['map_two']['team_1']['player_5']['name'][:8]:<8}:` `{game['map_two']['team_1']['player_5']['acs']:^5}` `{game['map_two']['team_1']['player_5']['kills']:^5}/{game['map_two']['team_1']['player_5']['deaths']:^5}/{game['map_two']['team_1']['player_5']['assists']:^5}` `{game['map_two']['team_1']['player_5']['adr']:^5}` `{game['map_two']['team_1']['player_5']['hs']:^5}`\n\n",

            f"**{game['map_two']['team_2']['team_name']}**",
            "`{:<8}:` `{:^5}` `{:^17}` `{:^5}` `{:^5}`".format('Name', 'ACS', 'K/D/A', 'ADR', 'HS%'),
            f"`{game['map_two']['team_2']['player_1']['name'][:8]:<8}:` `{game['map_two']['team_2']['player_1']['acs']:^5}` `{game['map_two']['team_2']['player_1']['kills']:^5}/{game['map_two']['team_2']['player_1']['deaths']:^5}/{game['map_two']['team_2']['player_1']['assists']:^5}` `{game['map_two']['team_2']['player_1']['adr']:^5}` `{game['map_two']['team_2']['player_1']['hs']:^5}`",
            f"`{game['map_two']['team_2']['player_2']['name'][:8]:<8}:` `{game['map_two']['team_2']['player_2']['acs']:^5}` `{game['map_two']['team_2']['player_2']['kills']:^5}/{game['map_two']['team_2']['player_2']['deaths']:^5}/{game['map_two']['team_2']['player_2']['assists']:^5}` `{game['map_two']['team_2']['player_2']['adr']:^5}` `{game['map_two']['team_2']['player_2']['hs']:^5}`",
            f"`{game['map_two']['team_2']['player_3']['name'][:8]:<8}:` `{game['map_two']['team_2']['player_3']['acs']:^5}` `{game['map_two']['team_2']['player_3']['kills']:^5}/{game['map_two']['team_2']['player_3']['deaths']:^5}/{game['map_two']['team_2']['player_3']['assists']:^5}` `{game['map_two']['team_2']['player_3']['adr']:^5}` `{game['map_two']['team_2']['player_3']['hs']:^5}`",
            f"`{game['map_two']['team_2']['player_4']['name'][:8]:<8}:` `{game['map_two']['team_2']['player_4']['acs']:^5}` `{game['map_two']['team_2']['player_4']['kills']:^5}/{game['map_two']['team_2']['player_4']['deaths']:^5}/{game['map_two']['team_2']['player_4']['assists']:^5}` `{game['map_two']['team_2']['player_4']['adr']:^5}` `{game['map_two']['team_2']['player_4']['hs']:^5}`",
            f"`{game['map_two']['team_2']['player_5']['name'][:8]:<8}:` `{game['map_two']['team_2']['player_5']['acs']:^5}` `{game['map_two']['team_2']['player_5']['kills']:^5}/{game['map_two']['team_2']['player_5']['deaths']:^5}/{game['map_two']['team_2']['player_5']['assists']:^5}` `{game['map_two']['team_2']['player_5']['adr']:^5}` `{game['map_two']['team_2']['player_5']['hs']:^5}`",
            ]
        map_three_list = [
            '`{:^21}`'.format('Game Info'),
            '`{:<8}:` `{:^5}:{:^5}`'.format('F-Score', game['team_1_score'], game['team_2_score']),
            '`{:<8}:` `{:^5}:{:^5}`'.format('M-Score', game['map_three']['team_1_score'], game['map_three']['team_2_score']),
            '`{:<8}:` `{:^11}`'.format('Map Pick', game['map_three']['map_name']),
            '`{:<8}:` `{:^11}`'.format('Duration', game['map_three']['map_duration']),
            '`{:<8}:` `{:^11}`'.format('Page', 'Match Three') + '\n',


            f"**{game['map_three']['team_1']['team_name']}**",
            "`{:<8}:` `{:^5}` `{:^17}` `{:^5}` `{:^5}`".format('Name', 'ACS', 'K/D/A', 'ADR', 'HS%'),
            f"`{game['map_three']['team_1']['player_1']['name'][:8]:<8}:` `{game['map_three']['team_1']['player_1']['acs']:^5}` `{game['map_three']['team_1']['player_1']['kills']:^5}/{game['map_three']['team_1']['player_1']['deaths']:^5}/{game['map_three']['team_1']['player_1']['assists']:^5}` `{game['map_three']['team_1']['player_1']['adr']:^5}` `{game['map_three']['team_1']['player_1']['hs']:^5}`",
            f"`{game['map_three']['team_1']['player_2']['name'][:8]:<8}:` `{game['map_three']['team_1']['player_2']['acs']:^5}` `{game['map_three']['team_1']['player_2']['kills']:^5}/{game['map_three']['team_1']['player_2']['deaths']:^5}/{game['map_three']['team_1']['player_2']['assists']:^5}` `{game['map_three']['team_1']['player_2']['adr']:^5}` `{game['map_three']['team_1']['player_2']['hs']:^5}`",
            f"`{game['map_three']['team_1']['player_3']['name'][:8]:<8}:` `{game['map_three']['team_1']['player_3']['acs']:^5}` `{game['map_three']['team_1']['player_3']['kills']:^5}/{game['map_three']['team_1']['player_3']['deaths']:^5}/{game['map_three']['team_1']['player_3']['assists']:^5}` `{game['map_three']['team_1']['player_3']['adr']:^5}` `{game['map_three']['team_1']['player_3']['hs']:^5}`",
            f"`{game['map_three']['team_1']['player_4']['name'][:8]:<8}:` `{game['map_three']['team_1']['player_4']['acs']:^5}` `{game['map_three']['team_1']['player_4']['kills']:^5}/{game['map_three']['team_1']['player_4']['deaths']:^5}/{game['map_three']['team_1']['player_4']['assists']:^5}` `{game['map_three']['team_1']['player_4']['adr']:^5}` `{game['map_three']['team_1']['player_4']['hs']:^5}`",
            f"`{game['map_three']['team_1']['player_5']['name'][:8]:<8}:` `{game['map_three']['team_1']['player_5']['acs']:^5}` `{game['map_three']['team_1']['player_5']['kills']:^5}/{game['map_three']['team_1']['player_5']['deaths']:^5}/{game['map_three']['team_1']['player_5']['assists']:^5}` `{game['map_three']['team_1']['player_5']['adr']:^5}` `{game['map_three']['team_1']['player_5']['hs']:^5}`\n\n",

            f"**{game['map_three']['team_2']['team_name']}**",
            "`{:<8}:` `{:^5}` `{:^17}` `{:^5}` `{:^5}`".format('Name', 'ACS', 'K/D/A', 'ADR', 'HS%'),
            f"`{game['map_three']['team_2']['player_1']['name'][:8]:<8}:` `{game['map_three']['team_2']['player_1']['acs']:^5}` `{game['map_three']['team_2']['player_1']['kills']:^5}/{game['map_three']['team_2']['player_1']['deaths']:^5}/{game['map_three']['team_2']['player_1']['assists']:^5}` `{game['map_three']['team_2']['player_1']['adr']:^5}` `{game['map_three']['team_2']['player_1']['hs']:^5}`",
            f"`{game['map_three']['team_2']['player_2']['name'][:8]:<8}:` `{game['map_three']['team_2']['player_2']['acs']:^5}` `{game['map_three']['team_2']['player_2']['kills']:^5}/{game['map_three']['team_2']['player_2']['deaths']:^5}/{game['map_three']['team_2']['player_2']['assists']:^5}` `{game['map_three']['team_2']['player_2']['adr']:^5}` `{game['map_three']['team_2']['player_2']['hs']:^5}`",
            f"`{game['map_three']['team_2']['player_3']['name'][:8]:<8}:` `{game['map_three']['team_2']['player_3']['acs']:^5}` `{game['map_three']['team_2']['player_3']['kills']:^5}/{game['map_three']['team_2']['player_3']['deaths']:^5}/{game['map_three']['team_2']['player_3']['assists']:^5}` `{game['map_three']['team_2']['player_3']['adr']:^5}` `{game['map_three']['team_2']['player_3']['hs']:^5}`",
            f"`{game['map_three']['team_2']['player_4']['name'][:8]:<8}:` `{game['map_three']['team_2']['player_4']['acs']:^5}` `{game['map_three']['team_2']['player_4']['kills']:^5}/{game['map_three']['team_2']['player_4']['deaths']:^5}/{game['map_three']['team_2']['player_4']['assists']:^5}` `{game['map_three']['team_2']['player_4']['adr']:^5}` `{game['map_three']['team_2']['player_4']['hs']:^5}`",
            f"`{game['map_three']['team_2']['player_5']['name'][:8]:<8}:` `{game['map_three']['team_2']['player_5']['acs']:^5}` `{game['map_three']['team_2']['player_5']['kills']:^5}/{game['map_three']['team_2']['player_5']['deaths']:^5}/{game['map_three']['team_2']['player_5']['assists']:^5}` `{game['map_three']['team_2']['player_5']['adr']:^5}` `{game['map_three']['team_2']['player_5']['hs']:^5}`",
            ]
        
        embed = nextcord.Embed(title=game['tournament_name'], description='\n'.join(all_stat_list), url="https://www.twitch.tv/valorant")
        embed.set_footer(text=f"Status: {game['start']} | {game['start_date']}")
        embed.set_thumbnail(url=game['tournament_pic'])

        await ctx.send(embed=embed, view=VLRPage(embed, all_stat_list, map_one_list, map_two_list, map_three_list))

def setup(client):
    client.add_cog(TextVLR(client))