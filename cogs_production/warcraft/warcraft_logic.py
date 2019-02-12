"""
Author:         David Schaeffer
Creation Date:  November 6, 2018
Purpose:        Defines methods used for much of the logic and data manipulation needed in
                the Warcraft module.
"""

from datetime import datetime
from operator import itemgetter
from urllib import parse

import discord
import requests
from bs4 import BeautifulSoup
from dateutil.tz import tz

from casper_utilities import utilities
from cogs_production.warcraft.warcraft_config import BlizzardAPI, WarcraftMedia


async def get_blizzard_access_token():
    url = (f'https://us.battle.net/oauth/token?grant_type='
           f'client_credentials&client_id={BlizzardAPI.CLIENT_ID}'
           f'&client_secret={BlizzardAPI.CLIENT_SECRET}')
    try:
        token = await utilities.json_get(url)
        return token
    except KeyError as e:
        print(f'Error attempting to generate access token:\n{e}')
        return None


async def get_raiderio_data(name: str, realm: str = 'wyrmrest-accord', region: str = 'us'):
    url = (f'https://raider.io/api/v1/characters/profile?region={region}&realm={realm}'
           f'&name={parse.quote(name).lower()}&fields=raid_progression,mythic_plus_scores,'
           f'mythic_plus_ranks,mythic_plus_recent_runs,mythic_plus_highest_level_runs,'
           f'mythic_plus_weekly_highest_level_runs,previous_mythic_plus_scores,'
           f'previous_mythic_plus_ranks')
    try:
        return await utilities.json_get(url)
    except Exception as e:
        print(f'Error while fetching Raider.IO data:\n{e}')
        return None


async def get_blizzard_data(name: str, realm: str = 'wyrmrest-accord', region: str = 'us'):
    token = await get_blizzard_access_token()
    if token is not None:
        url = (f'https://{region}.api.blizzard.com/wow/character/{realm}/'
               f'{parse.quote(name).lower()}?'
               f'fields=guild,items,pvp,achievements&locale=en_US'
               f'&access_token={token["access_token"]}')
        try:
            return await utilities.json_get(url)
        except Exception as e:
            print(f'Error while fetching Blizzard data:\n{e}')
            return None


async def convert_utc_to_local(utc_time):
    local_time = datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S')
    local_time = local_time.replace(tzinfo=tz.tzutc())
    local_time = local_time.astimezone(tz.tzlocal())
    return local_time


async def scrape_prestige(name: str, realm: str = 'wyrmrest-accord', region: str = 'us'):
    url = (f'https://worldofwarcraft.com/en-{region}/character/'
           f'{realm.replace(" ", "-")}/{parse.quote(name).lower()}/pvp')
    resp = requests.get(url)
    if resp.status_code == 200:
        try:
            raw_html = BeautifulSoup(resp.text, 'html5lib')
            prestige_div = raw_html.find('div', text='Honor')
            prestige_text = prestige_div.find_next_sibling().find_next_sibling().text
            return prestige_text.replace('Level ', '')
        except AttributeError as e:
            print(f'An error occurred while extracting prestige level:\n{e}')
            return None
    else:
        print(f'An error occurred while extracting prestige level for:\n{url}')
        return None


async def get_blizzard_token_price(region: str = 'us'):
    token = await get_blizzard_access_token()
    if token is not None:
        url = (f'https://{region}.api.blizzard.com/data/wow/token/'
               f'?namespace={WarcraftMedia.region_codes[region]["namespace"]}'
               f'&locale={WarcraftMedia.region_codes[region]["locale"]}'
               f'&access_token={token["access_token"]}')
        try:
            resp_json = await utilities.json_get(url)
            return int((resp_json['price'] / 100) / 100)
        except Exception as e:
            print(f'Error while fetching Blizzard token price.\n{e}')
            return None
    else:
        return None


async def get_guild_members(guild_name: str='felforged-covenant', realm: str='wyrmrest-accord',
                            ranks: list=None):
    token = await get_blizzard_access_token()
    if token is not None:
        url = (f'https://us.api.blizzard.com/wow/guild/{realm}/'
               f'{parse.quote(guild_name.replace("-", " "))}?fields=members&locale=en_US'
               f'&access_token={token["access_token"]}')
        results = await utilities.json_get(url)
        if results is None:
            return None
        if ranks is None:
            members = [(member['character']['name'], member['character']['realm'], member['rank']) for member in results['members']
                       if member['character']['level'] == 120]
        else:
            members = [(member['character']['name'], member['character']['realm'], member['rank']) for member in results['members']
                       if member['rank'] in ranks and member['character']['level'] == 120]
            members = sorted(members, key=itemgetter(2))
        return members


async def get_mplus_counts(names: str):
    plus_2_achieve = 33096
    wqs_50_complete = 33094
    total_num_runs = 0
    total_world_quests = 0
    total_boss_kills = 0
    names = names.split(' ')
    out_msg = ('```\n'
               f'{"Character":{14}}{"M+":<{5}}{"WQs":<{6}}'
               f'{"Bosses":<{7}}\n\n')
    token = await get_blizzard_access_token()
    if token is not None:
        for name in names:
            char_mplus_runs = 0
            char_wqs = 0
            char_boss_kills = 0
            character_url = (f'https://us.api.blizzard.com/wow/character/'
                             f'wyrmrest-accord/{name.lower()}'
                             f'?fields=achievements,progression'
                             f'&locale=en_US'
                             f'&access_token={token["access_token"]}')
            results = await utilities.json_get(character_url)
            try:
                criteria_index = results['achievements']['criteria'].index(plus_2_achieve)
                char_mplus_runs = results['achievements']['criteriaQuantity'][criteria_index]
                total_num_runs += results['achievements']['criteriaQuantity'][criteria_index]

                criteria_index = results['achievements']['criteria'].index(wqs_50_complete)
                char_wqs = results['achievements']['criteriaQuantity'][criteria_index]
                total_world_quests += results['achievements']['criteriaQuantity'][criteria_index]

                current_raids = ['The Emerald Nightmare', 'Trial of Valor',
                                 'The Nighthold', 'Tomb of Sargeras', 'Antorus, the Burning Throne']
                raid_results = [raid for raid in results['progression']['raids']
                                if raid['name'] in current_raids]
                for raid in raid_results:
                    for boss in raid['bosses']:
                        char_boss_kills += boss['lfrKills']
                        char_boss_kills += boss['normalKills']
                        char_boss_kills += boss['heroicKills']
                        char_boss_kills += boss['mythicKills']
                total_boss_kills += char_boss_kills
                out_msg += (f'{name.title():{14}}{char_mplus_runs:<{5}}'
                            f'{char_wqs:<{6}}{char_boss_kills:<{7}}\n')
            except KeyError:
                out_msg += (f'{name.title():{14}}{"Err":<{5}}'
                            f'{"Err":<{6}}{"Err":<{7}}\n')
        out_msg += (f'---------------------------------\n'
                    f'{"Total":{14}}{total_num_runs:<{5}}'
                    f'{total_world_quests:<{6}}{total_boss_kills:<{7}}\n'
                    f'```')
        return out_msg
    return 'Could not fetch access token.'


"""
                           MESSAGE OUTPUTS
"""


async def build_embed_obj(raiderio_data: dict, blizzard_data: dict, honor_level: int):
    # for k, v in raiderio_data.items():
    #     print(f'{k}: {v}')
    # print('==============================================\n=============================')
    # for k, v in blizzard_data.items():
    #     print(f'{k}: {v}')
    embed_obj = discord.Embed()
    embed_obj.colour = WarcraftMedia.class_colors[raiderio_data['class']]
    embed_obj.set_thumbnail(url=raiderio_data['thumbnail_url'])
    embed_obj.title = f'{raiderio_data["name"]}'
    if 'guild' in blizzard_data.keys():
        guild_name = f'<{blizzard_data["guild"]["name"]}> - '
    else:
        guild_name = ''
    embed_obj.add_field(
        name=f'{guild_name}{blizzard_data["realm"]}',
        value=f'{raiderio_data["race"]} {raiderio_data["active_spec_name"]} {raiderio_data["class"]}\n'
              f'**ilvl:** {blizzard_data["items"]["averageItemLevelEquipped"]}\n'
              f'Heart of Azeroth Level: {blizzard_data["items"]["neck"]["azeriteItem"]["azeriteLevel"]}\n'
              f'[Battle.net Profile](https://worldofwarcraft.com/en-us/character/'
              f'{blizzard_data["realm"].replace(" ", "-")}/'
              f'{raiderio_data["name"]})')

    # RAID PROGRESSION
    embed_obj.add_field(name='__**Raid Progression:**__',
                        value=(f'**UD:** {raiderio_data["raid_progression"]["uldir"]["summary"]:{12}}'
                               f'**BoD:** {raiderio_data["raid_progression"]["battle-of-dazaralor"]["summary"]:{12}}'),
                        inline=False)

    # MYTHIC+ PROGRESSION
    if len(raiderio_data['mythic_plus_highest_level_runs']) != 0:
        mins, secs = divmod(
            raiderio_data["mythic_plus_highest_level_runs"][0]["clear_time_ms"] / 1000,
            60)
        clear_date_local = await convert_utc_to_local(
            raiderio_data["mythic_plus_highest_level_runs"][0]["completed_at"].replace(
                'T', ' ')[:-5])

        # OVERALL MYTHIC+ PROGRESSION
        embed_obj.add_field(name='__**Mythic+ Progression:**__',
                            value=f'**Current Season Score:** {raiderio_data["mythic_plus_scores"]["all"]:,}\n'
                                  f'**Realm Rank:** #{raiderio_data["mythic_plus_ranks"]["overall"]["realm"]:,} '
                                  f'(#{raiderio_data["mythic_plus_ranks"]["class"]["realm"]:,} '
                                  f'for {raiderio_data["class"]}s)\n'
                                  f'Highest Run: {raiderio_data["mythic_plus_highest_level_runs"][0]["dungeon"]} '
                                  f'+{raiderio_data["mythic_plus_highest_level_runs"][0]["mythic_level"]} cleared in '
                                  f'{mins}:{secs:.1f} upgrading the key '
                                  f'{raiderio_data["mythic_plus_highest_level_runs"][0]["num_keystone_upgrades"]} '
                                  f'time(s) for a score of {raiderio_data["mythic_plus_highest_level_runs"][0]["score"]}.\n'
                                  f'Completed on {clear_date_local}.\n'
                                  f'[Run Info]({raiderio_data["mythic_plus_highest_level_runs"][0]["url"]})\n'
                                  f'[Raider.io Profile]({raiderio_data["profile_url"]})',
                            inline=False)

        # WEEKLY MYTHIC+ PROGRESSION
        if len(raiderio_data['mythic_plus_weekly_highest_level_runs']) != 0:
            mins, secs = divmod(raiderio_data["mythic_plus_weekly_highest_level_runs"][0][
                                    "clear_time_ms"] / 1000, 60)
            clear_date_local = await convert_utc_to_local(
                raiderio_data["mythic_plus_weekly_highest_level_runs"][0][
                    "completed_at"].replace('T', ' ')[:-5])
            embed_obj.add_field(name='__**Weekly High Mythic+ Run:**__',
                                value=f'{raiderio_data["mythic_plus_weekly_highest_level_runs"][0]["dungeon"]} '
                                      f'+{raiderio_data["mythic_plus_weekly_highest_level_runs"][0]["mythic_level"]} cleared in '
                                      f'{mins}:{secs:.1f} upgrading the key '
                                      f'{raiderio_data["mythic_plus_weekly_highest_level_runs"][0]["num_keystone_upgrades"]} '
                                      f'time(s) for a score of {raiderio_data["mythic_plus_weekly_highest_level_runs"][0]["score"]}.\n'
                                      f'Completed on {clear_date_local}.\n'
                                      f'[Run Info]({raiderio_data["mythic_plus_weekly_highest_level_runs"][0]["url"]})', inline=False)

        # MOST RECENT MYTHIC+ PROGRESSION
        elif len(raiderio_data['mythic_plus_recent_runs']) != 0:
            mins, secs = divmod(
                raiderio_data["mythic_plus_recent_runs"][0]["clear_time_ms"] / 1000, 60)
            clear_date_local = await convert_utc_to_local(
                raiderio_data["mythic_plus_recent_runs"][0]["completed_at"].replace('T',
                                                                                    ' ')[
                :-5])
            embed_obj.add_field(
                name='__**Most Recent Mythic+ Run:**__ (No run found this week)',
                value=f'{raiderio_data["mythic_plus_recent_runs"][0]["dungeon"]} '
                      f'+{raiderio_data["mythic_plus_recent_runs"][0]["mythic_level"]} cleared in '
                      f'{mins}:{secs:.1f} upgrading the key '
                      f'{raiderio_data["mythic_plus_recent_runs"][0]["num_keystone_upgrades"]} '
                      f'time(s) for a score of {raiderio_data["mythic_plus_recent_runs"][0]["score"]}.\n'
                      f'Completed on {clear_date_local}.\n'
                      f'[Run Info]({raiderio_data["mythic_plus_recent_runs"][0]["url"]})', inline=False)
    else:
        # HISTORIC MYTHIC+ SCORES?
        try:
            embed_obj.add_field(name='__**Mythic+ Progression:**__',
                                value=f'No mythic+ data could be found for this character '
                                      f'this season.\n'
                                      f'[Raider.io Profile]({raiderio_data["profile_url"]})',
                                inline=False)
        # NO MYTHIC+ EVER
        except KeyError as e:
            print(f'An error occurred while attempting to fetch best m+ score.:\n{e}')
            embed_obj.add_field(name='__**Mythic+ Progression:**__',
                                value=f'No mythic+ data could be found for this character '
                                      f'this season.\n'
                                      f'[Raider.io Profile]({raiderio_data["profile_url"]})',
                                inline=False)
    # Prestige level is not available via API, we're scraping the pvp page for it.
    if honor_level is not None:
        embed_obj.add_field(name='__**PvP Progression**__',
                            value=f'**Honor Level:** {honor_level}\n'
                                  f'2v2 Rating: {blizzard_data["pvp"]["brackets"]["ARENA_BRACKET_2v2"]["rating"]}\n'
                                  f'3v3 Rating: {blizzard_data["pvp"]["brackets"]["ARENA_BRACKET_3v3"]["rating"]}\n'
                                  f'RBG Rating: {blizzard_data["pvp"]["brackets"]["ARENA_BRACKET_RBG"]["rating"]}\n',
                            inline=False)
    else:
        embed_obj.add_field(name='__**PvP Progression**__',
                            value=f'**Honor Level:** Broken Blizz armory. gg\n'
                                  f'2v2 Rating: {blizzard_data["pvp"]["brackets"]["ARENA_BRACKET_2v2"]["rating"]}\n'
                                  f'3v3 Rating: {blizzard_data["pvp"]["brackets"]["ARENA_BRACKET_3v3"]["rating"]}\n'
                                  f'RBG Rating: {blizzard_data["pvp"]["brackets"]["ARENA_BRACKET_RBG"]["rating"]}\n',
                            inline=False)
    embed_obj.add_field(name='__**Warcraft Logs:**__',
                        value=f'https://www.warcraftlogs.com/character/us/'
                              f'{raiderio_data["realm"].lower().replace(" ", "-")}/'
                              f'{raiderio_data["name"]}',
                        inline=False)
    return embed_obj


async def build_scores_output(characters: list, num: int=10):
    desc = (f'{"":{3}}{"Character:":{14}}{"Score:":{9}}'
            f'{"Realm:":{8}}{"Class:":}\n'
            f'--------------------------------------------\n')
    i = 1
    for character in characters:
        desc += (f'{i:<{3}}{character.name.title():{14}}'
                 f'{character.m_plus_score_overall:<{9}}'
                 f'{character.m_plus_rank_overall:<{8}}'
                 f'{character.m_plus_rank_class}'
                 f' - {character.char_class.title():<}\n')
        if i == num:
            break
        i += 1
    description = f'```{desc}```'
    return description


async def build_honor_output(characters: list, num: int=10):
    desc = (f'{"":{3}}{"Character:":{16}}{"Honor Level:":{10}}\n'
            f'---------------------------------------------------\n')
    i = 1
    for character in characters:
        desc += (f'{i:<{3}}{character.name.title():{16}}'
                 f'{character.honor_level:<{10}}\n')
        if i == num:
            break
        i += 1
    description = f'```{desc}```'
    return description


async def build_readycheck(guild_members: list):
    rank_names = {0: 'GM', 1: 'Officer', 3: 'Raider', 7: 'Trial'}
    total_ilvl = 0
    member_count = 0
    output_msg_text = (f'```{"Name:":{14}}{"Rank:":{8}}{"HoA:":{6}}{"Weekly M+:":{11}}'
                       f'{"ilvl:":{6}}\n'
                       f'--------------------------------------------\n')
    for member in guild_members:
        total_ilvl += member.ilvl
        member_count += 1
        output_msg_text += (f'{member.name.title():{14}}'
                            f'{rank_names[member.guild_rank]:{8}}'
                            f'{member.heart_of_azeroth_level:<{6}}'
                            f'{member.m_plus_weekly_high:<{11}}'
                            f'{member.ilvl}\n')
    avg_ilvl = round(total_ilvl/member_count)
    output_msg_text += ('--------------------------------------------\n'
                        f'{"Avg ilvl:":{39}}{avg_ilvl:<{6}}\n\n'
                        'Remember: You need to clear a +10 (not necessarily in time) '
                        'to maximize the loot from your weekly chest.```')
    return output_msg_text
