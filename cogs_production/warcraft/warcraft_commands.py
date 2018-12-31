"""
Author:         David Schaeffer
Creation Date:  November 6, 2018
Purpose:        Defines all commands for the Warcraft module
"""

import discord
import requests
from cogs_development.warcraft.warcraft_config import WarcraftMedia
from discord.ext import commands

from cogs_production.warcraft import warcraft_logic
# import database, which imports engine and the models, which instantiates everything
from database.warcraftcharacters import WarcraftCharactersDatabaseMethods


class Warcraft:
    def __init__(self, casper):
        self.casper = casper
        self.blacklist_ids = [228366233504972810]  # aiirie
        self.blacklist_names = ['illyre', 'aiirie']

        @self.casper.event
        async def on_message(msg):
            if msg.author.id in self.blacklist_ids:
                return
            await self.casper.process_commands(msg)

    @commands.command()
    async def crawl(self, ctx, claim: str='no', guild_name: str='felforged',
                    realm: str='wyrmrest-accord'):
        """
        Crawls a given guild, looking up it's members and adding them to the database.
        :param ctx: command call context.
        :param claim: Whether to claim the guild as belonging to this discord server.
        :param guild_name: The guild name to lookup.
        :param realm: The realm the guild resides on.
        :return: A message pertaining to the status of the crawl.
        """
        message = await ctx.send('Beginning...')
        guild_members = await warcraft_logic.get_guild_members(guild_name, realm)
        if guild_members is None:
            return await message.edit(content='Could not fetch members from Blizzard.')
        char_index = 1
        for name, realm, rank in guild_members:
            if name.lower() in self.blacklist_names:
                continue
            try:
                raiderio_data = await warcraft_logic.get_raiderio_data(name, realm, 'us')
                blizzard_data = await warcraft_logic.get_blizzard_data(name, realm, 'us')
                honor_level = await warcraft_logic.scrape_prestige(name, realm)
                if await WarcraftCharactersDatabaseMethods.character_exists(name, realm):
                    await WarcraftCharactersDatabaseMethods.update_character(raiderio_data, blizzard_data, honor_level, rank)
                else:
                    await WarcraftCharactersDatabaseMethods.create_new_character(raiderio_data, blizzard_data, honor_level, rank)
                if 'yes' in claim.lower():
                    await WarcraftCharactersDatabaseMethods.claim_character(name, realm, ctx.guild.id)
            except Exception as e:
                print('Error: ', e)
            char_index += 1
            if char_index % 5 == 0:
                await message.edit(content=f'{char_index}/{guild_members.__len__()} '
                                           f'characters crawled.')
        return await message.edit(content='Finished crawling.')

    @commands.command()
    async def wow(self, ctx, name: str, realm: str='wyrmrest-accord', region: str='us'):
        """
        Looks up an individual character.
        :param ctx: command call context.
        :param name: The name of the character.
        :param realm: The realm the character resides on.
        :param region: The region of the character.
        :return: An Embed object with the details of the character.
        """
        status_msg = await ctx.send('Fetching character data...')
        blizzard_data = await warcraft_logic.get_blizzard_data(name, realm, region)
        if blizzard_data is None:
            return await status_msg.edit(content='Could not fetch character from '
                                                 'Blizzard.')
        raiderio_data = await warcraft_logic.get_raiderio_data(name, realm, region)
        if raiderio_data is None:
            return await status_msg.edit(content='Could not find character profile on '
                                                 'Raider.io.')
        # print(raiderio_data)
        # print(blizzard_data)
        honor_level = await warcraft_logic.scrape_prestige(name, realm, region)
        if await WarcraftCharactersDatabaseMethods.character_exists(name, realm):
            await WarcraftCharactersDatabaseMethods.update_character(raiderio_data, blizzard_data, honor_level)
        else:
            await WarcraftCharactersDatabaseMethods.create_new_character(raiderio_data, blizzard_data, honor_level)
        embed_obj = await warcraft_logic.build_embed_obj(raiderio_data, blizzard_data, honor_level)
        return await status_msg.edit(content='', embed=embed_obj)

    @commands.command()
    async def readycheck(self, ctx, sort_by: str='rank'):
        """
        Get a list of raider details.
        :param ctx:
        :param sort_by: Options are: rank, ilvl, mplus, hoa
        :return: A sorted list of raiders
        """
        ranks = [0, 1, 3, 7]
        sent_msg = await ctx.send('Fetching raiders and trials...')
        guild_members = await WarcraftCharactersDatabaseMethods.get_raiders(ctx.guild.id, ranks, sort_by)
        await sent_msg.edit(content='Parsing data...')
        output_msg_text = await warcraft_logic.build_readycheck(guild_members)
        return await sent_msg.edit(content=output_msg_text)

    @commands.command()
    async def mplus(self, ctx, *, names: str):
        """
        Given a space-separated list of character names, will lookup how many mythic
        plus, world quests, and raid bosses the characters have killed.
        :param ctx:
        :param names:
        :return:
        """
        output = await warcraft_logic.get_mplus_counts(names)
        return await ctx.send(output)

    @commands.command()
    async def claim(self, ctx, name: str, realm: str='wyrmrest-accord'):
        if await WarcraftCharactersDatabaseMethods.character_exists(name, realm):
            await WarcraftCharactersDatabaseMethods.claim_character(name, realm, ctx.guild.id)
            return await ctx.send(f'{name.title()}-{realm.replace("-", " ").capitalize()} has been claimed.')
        else:
            return await ctx.send(f'{name.title()}-{realm.replace("-", " ").capitalize()} has not been seen yet.)')

    @commands.command()
    async def scores(self, ctx, num=10):
        """
        Displays m+ scores for all characters claimed on this server. See
        'claim' command.
        :param ctx:
        :return:
        """
        characters = await WarcraftCharactersDatabaseMethods.get_scores(ctx.guild.id)
        if num > 25:
            num = 25
        if len(characters) > 0:
            description = await warcraft_logic.build_scores_output(characters, num)
            return await ctx.send(description)

    @commands.command()
    async def honor(self, ctx, num=10):
        """
        Displays honor level for all characters claimed on this server. See
        'claim' command.
        :param ctx:
        :return:
        """
        characters = await WarcraftCharactersDatabaseMethods.get_honor_levels(ctx.guild.id)
        if num > 25:
            num = 25
        if len(characters) > 0:
            description = await warcraft_logic.build_honor_output(characters, num)
            return await ctx.send(description)

    @commands.command()
    async def addkey(self, ctx, name: str, key_info: str=None):
        if key_info is None:
            return await ctx.send('Don\'t forget to include your charater name.\n'
                                  '`casper addkey charName brh+8`')
        if '+' not in key_info:
            return await ctx.send('Don\'t forget to format your key correctly.\n'
                                  '`brh+8`')
        dungeon, level = key_info.lower().split('+')
        if int(level) < 2:
            return await ctx.send('The key level must be greater than 1.')
        if dungeon in WarcraftMedia.m_plus_abbreviations_bfa.keys():
            dungeon_name = WarcraftMedia.m_plus_abbreviations_bfa[dungeon]
        else:
            out_str = ('Dungeon not recognized. Make sure you\'re using the '
                       'proper abbreviation:\n')
            for key in WarcraftMedia.m_plus_abbreviations_bfa.keys():
                out_str += f'{key}, '
            return await ctx.send(out_str)
        if await WarcraftCharactersDatabaseMethods.character_exists(name, 'wyrmrest-accord'):
            await WarcraftCharactersDatabaseMethods.add_key(name, dungeon_name, level)
        else:
            return await ctx.send('That character does not exist.')
        return await ctx.invoke(self.keys)

    @commands.command()
    async def removekey(self, ctx, name: str):
        if await WarcraftCharactersDatabaseMethods.character_exists(name, 'wyrmrest-accord'):
            await WarcraftCharactersDatabaseMethods.remove_key(name)
            return await ctx.invoke(self.keys)
        else:
            return await ctx.send('Character not found.')

    @commands.command()
    async def keys(self, ctx):
        characters = await WarcraftCharactersDatabaseMethods.get_keys(ctx.guild.id)
        if len(characters) > 0:
            desc = f'{"Character:":{14}}{"Dungeon:":{27}}{"Level:":{6}}\n' \
                   f'------------------------------------------------\n'
            for character in characters:
                desc += f'{character.name.title():{14}}' \
                        f'{character.m_plus_key:{27}} ' \
                        f'+{character.m_plus_key_level:<{6}}\n'
            await ctx.send(f'```{desc}```')

    @commands.command()
    async def resetkeys(self, ctx):
        await WarcraftCharactersDatabaseMethods.reset_keys()
        return await ctx.send('Key info has been reset.')

    @commands.command()
    async def token(self, ctx, region: str='us'):
        try:
            token_price = await warcraft_logic.get_blizzard_token_price(region)
            if token_price is not None:
                return await ctx.send(f'Tokens currently cost {token_price:,} gold in the'
                                      f' {region.upper()} region.')
        except KeyError as e:
            return await ctx.send('Could not retrieve token price for that region. '
                                  'Possible regions are: ```us, eu, tw, kr```')

    @commands.command()
    async def affixes(self, ctx, region='us', locale='en'):
        """
        Displays the weekly mythic+ affixes for a given region.
        Ex: casper affixes, casper affixes eu
        :param ctx: The invocation context
        :param region: The region to get affixes for
        :param locale: The locale to retrieve data in
        :return: The weekly affixes and their descriptions
        """
        url = (f'https://raider.io/api/v1/mythic-plus/affixes'
               f'?region={region}'
               f'&locale={locale}')
        response = requests.request('GET', url).json()['affix_details']
        output_embed = discord.Embed()
        output_embed.title = f'__Weekly M+ Affixes for {region.upper()}:__'
        for dict_affix in response:
            output_embed.add_field(name=f'{dict_affix["name"]}:',
                                   value=f'{dict_affix["description"]}')
        return await ctx.send(embed=output_embed)

    @commands.command()
    async def classhelp(self, ctx, *, _class):
        """
        Returns a permalink to a given class's discord server.
        ex: casper classhelp dk, casper classhelp demon-hunter, casper classhelp
        death knight
        """
        if _class is None:
            return await ctx.send('Don\'t forget the class name at the end!\n'
                                  '```casper classhelp mage```')
        _class = _class.lower()
        if _class in ['death knight', 'death-knight', 'dk']:
            return await ctx.send('https://discord.gg/acherus')
        if _class in ['demon hunter', 'demon-hunter', 'dh']:
            return await ctx.send('https://discord.gg/zGGkNGC')
        if _class in ['druid']:
            return await ctx.send('https://discord.gg/0dWu0WkuetF87H9H')
        if _class in ['hunter']:
            return await ctx.send('https://discord.gg/yqer4BX')
        if _class in ['mage']:
            return await ctx.send('https://discord.me/alteredtime')
        if _class in ['monk']:
            return await ctx.send('http://discord.gg/peakofserenity')
        if _class in ['pally', 'paladin']:
            return await ctx.send('https://discord.gg/0dvRDgpa5xZHFfnD')
        if _class in ['priest']:
            return await ctx.send('https://discord.gg/HowToPriest')
        if _class in ['rogue', 'rouge']:
            return await ctx.send('https://discord.gg/0h08tydxoNhfDVZf')
        if _class in ['shaman']:
            return await ctx.send('https://discord.gg/earthshrine')
        if _class in ['warlock', 'lock']:
            return await ctx.send('https://discord.gg/0onXDymd9Wpc2CEu')
        if _class in ['warrior', 'warr']:
            return await ctx.send('https://discord.gg/0pYY7932lTH4FHW6')
        return await ctx.send(f'Couldn\'t find **{_class}**.')


def setup(casper):
    casper.add_cog(Warcraft(casper))
