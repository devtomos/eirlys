import requests, re
from bs4 import BeautifulSoup
from lxml import etree
from typing import Dict
from src.api.general.wide_functions import convert

async def match(url: str) -> Dict:
    upcoming_req = requests.get(url)
    soup = BeautifulSoup(upcoming_req.content, "html.parser")
    tree = etree.HTML(str(soup))
    
    match_array = {
        'start': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/div/div[1]')])),
        'start_date': re.sub(r'([\n\t]+)', '', tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[1]')[0].text),
        'tournament_name': re.sub(r'([\n\t]+)', '', tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[1]/div[1]/a/div/div[1]')[0].text),
        'tournament_pic': re.sub(r'([\n\t]+)', '', 'https:' + str(tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[1]/div[1]/a/img/@src')[0])),
        'team_1_score': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/div/div[2]/div[1]/span[1]')])),
        'team_2_score': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/div/div[2]/div[1]/span[3]')])),
        
        'all_stats': {
            'map_name': '-',
            'map_duration': '-',
            'team_1': {
                'team_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a[1]/div/div[1]')])),
                'player_1': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[11]/span/span[1]')])),
                },
                'player_2': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[11]/span/span[1]')])),
                },
                'player_3': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[11]/span/span[1]')])),
                },
                'player_4': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[11]/span/span[1]')])),
                },
                'player_5': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[11]/span/span[1]')])),
                }
            },
            'team_2': {
                'team_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a[2]/div/div[1]')])),
                'player_1': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[11]/span/span[1]')])),
                },
                'player_2': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[11]/span/span[1]')])),
                },
                'player_3': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[11]/span/span[1]')])),
                },
                'player_4': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[11]/span/span[1]')])),
                },
                'player_5': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[11]/span/span[1]')])),
                }
            },
        },

        'map_one': {
            'map_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[1]/div[2]/div[1]/span')])),
            'map_duration': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[1]/div[2]/div[2]')])),
            'team_1_score': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[1]/div[1]/div[1]')])),
            'team_2_score': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[1]/div[3]/div[2]')])),
            'team_1': {
                'team_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a[1]/div/div[1]')])),
                'player_1': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[1]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[1]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[1]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[1]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[1]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[1]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[1]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[1]/td[11]/span/span[1]')])),
                },
                'player_2': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[11]/span/span[1]')])),
                },
                'player_3': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[11]/span/span[1]')])),
                },
                'player_4': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[4]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[4]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[4]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[4]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[4]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[4]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[4]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[4]/td[11]/span/span[1]')])),
                },
                'player_5': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[11]/span/span[1]')])),
                }
            },
            'team_2': {
                'team_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a[2]/div/div[1]')])),
                'player_1': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[11]/span/span[1]')])),
                },
                'player_2': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[11]/span/span[1]')])),
                },
                'player_3': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[3]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[3]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[3]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[3]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[3]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[3]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[3]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[3]/td[11]/span/span[1]')])),
                },
                'player_4': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[4]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[4]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[4]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[4]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[4]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[4]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[4]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[4]/td[11]/span/span[1]')])),
                },
                'player_5': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[5]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[5]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[5]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[5]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[5]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[5]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[5]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[5]/td[11]/span/span[1]')])),
                }
            },
        },

        'map_two': {
            'map_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[1]/div[2]/div[1]/span')])),
            'map_duration': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[1]/div[2]/div[2]')])),
            'team_1_score': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[1]/div[1]/div[1]')])),
            'team_2_score': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[1]/div[3]/div[2]')])),
            'team_1': {
                'team_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a[1]/div/div[1]')])),
                'player_1': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[1]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[1]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[1]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[1]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[1]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[1]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[1]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[1]/td[11]/span/span[1]')])),
                },
                'player_2': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[2]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[2]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[2]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[2]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[2]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[2]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[2]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[2]/td[11]/span/span[1]')])),
                },
                'player_3': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[3]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[3]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[3]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[3]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[3]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[3]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[3]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[3]/td[11]/span/span[1]')])),
                },
                'player_4': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[4]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[4]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[4]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[4]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[4]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[4]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[4]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[4]/td[11]/span/span[1]')])),
                },
                'player_5': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[5]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[5]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[5]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[5]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[5]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[5]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[5]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[5]/td[11]/span/span[1]')])),
                }
            },
            'team_2': {
                'team_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a[2]/div/div[1]')])),
                'player_1': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[11]/span/span[1]')])),
                },
                'player_2': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[2]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[2]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[2]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[2]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[2]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[2]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[2]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[2]/td[11]/span/span[1]')])),
                },
                'player_3': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[3]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[3]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[3]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[3]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[3]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[3]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[3]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[3]/td[11]/span/span[1]')])),
                },
                'player_4': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[4]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[4]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[4]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[4]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[4]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[4]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[4]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[4]/td[11]/span/span[1]')])),
                },
                'player_5': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[5]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[5]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[5]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[5]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[5]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[5]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[5]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[4]/div[2]/table/tbody/tr[5]/td[11]/span/span[1]')])),
                }
            },
        },

        'map_three': {
            'map_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[1]/div[2]/div[1]/span')])),
            'map_duration': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[1]/div[2]/div[2]')])),
            'team_1_score': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[1]/div[1]/div[1]')])),
            'team_2_score': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[1]/div[3]/div[2]')])),
            'team_1': {
                'team_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a[1]/div/div[1]')])),
                'player_1': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[11]/span/span[1]')])),
                },
                'player_2': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[2]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[2]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[2]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[2]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[2]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[2]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[2]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[2]/td[11]/span/span[1]')])),
                },
                'player_3': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[3]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[3]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[3]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[3]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[3]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[3]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[3]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[3]/td[11]/span/span[1]')])),
                },
                'player_4': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[4]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[4]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[4]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[4]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[4]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[4]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[4]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[4]/td[11]/span/span[1]')])),
                },
                'player_5': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[5]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[5]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[5]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[5]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[5]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[5]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[5]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[1]/table/tbody/tr[5]/td[11]/span/span[1]')])),
                }
            },
            'team_2': {
                'team_name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a[2]/div/div[1]')])),
                'player_1': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[11]/span/span[1]')])),
                },
                'player_2': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[2]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[2]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[2]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[2]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[2]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[2]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[2]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[2]/td[11]/span/span[1]')])),
                },
                'player_3': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[3]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[3]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[3]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[3]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[3]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[3]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[3]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[3]/td[11]/span/span[1]')])),
                },
                'player_4': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[4]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[4]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[4]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[4]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[4]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[4]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[4]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[4]/td[11]/span/span[1]')])),
                },
                'player_5': {
                    'name': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[5]/td[1]/div/a/div[1]')])),
                    'acs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[5]/td[4]/span/span[1]')])),
                    'kills': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[5]/td[5]/span/span[1]')])),
                    'deaths': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[5]/td[6]/span/span[2]/span[1]')])),
                    'assists': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[5]/td[7]/span/span[1]')])),
                    'pon': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[5]/td[8]/span/span[1]')])),
                    'adr': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[5]/td[10]/span/span[1]')])),
                    'hs': re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[4]/div[2]/table/tbody/tr[5]/td[11]/span/span[1]')])),
                }
            },
        },
    }

    if match_array['all_stats']['team_1']['player_1']['name'] == '':
        for i in range(1, 6):
            match_array['all_stats']['team_1'][f'player_{i}']['name'] = re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath(f'/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div/div[1]/table/tbody/tr[{i}]/td[1]/div/a/div[1]')]))
    
    if match_array['all_stats']['team_2']['player_1']['name'] == '':
        for i in range(1, 6):
            match_array['all_stats']['team_2'][f'player_{i}']['name'] = re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath(f'/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div/div[2]/table/tbody/tr[{i}]/td[1]/div/a/div[1]')]))

    if match_array['map_one']['team_1']['player_1']['name'] == '':
        for i in range(1, 6):
            match_array['map_one']['team_1'][f'player_{i}']['name'] = re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath(f'/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[3]/div[1]/table/tbody/tr[{i}]/td[1]/div/a/div[1]')]))
    
    if match_array['map_one']['team_2']['player_1']['name'] == '':
        for i in range(1, 6):
            match_array['map_one']['team_2'][f'player_{i}']['name'] = re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath(f'/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[3]/div[2]/table/tbody/tr[{i}]/td[1]/div/a/div[1]')]))

    if match_array['map_two']['team_1']['player_1']['name'] == '':
        for i in range(1, 6):
            match_array['map_two']['team_1'][f'player_{i}']['name'] = re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath(f'/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[3]/div[1]/table/tbody/tr[{i}]/td[1]/div/a/div[1]')]))
    
    if match_array['map_two']['team_2']['player_1']['name'] == '':
        for i in range(1, 6):
            match_array['map_two']['team_2'][f'player_{i}']['name'] = re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath(f'/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[3]/div[3]/div[2]/table/tbody/tr[{i}]/td[1]/div/a/div[1]')]))

    if match_array['map_three']['team_1']['player_1']['name'] == '':
        for i in range(1, 6):
            match_array['map_three']['team_1'][f'player_{i}']['name'] = re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath(f'/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[3]/div[1]/table/tbody/tr[{i}]/td[1]/div/a/div[1]')]))
    
    if match_array['map_three']['team_2']['player_1']['name'] == '':
        for i in range(1, 6):
            match_array['map_three']['team_2'][f'player_{i}']['name'] = re.sub(r'([\n\t]+)', '', ''.join([x.text for x in tree.xpath(f'/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[4]/div[3]/div[2]/table/tbody/tr[{i}]/td[1]/div/a/div[1]')]))

    if match_array['start'] == '':
        match_array['start'] = 'LIVE'

    convert(match_array, tree)
    return match_array
