import datetime
from datetime import date

from sqlalchemy import desc, asc

from database.database_models import Character
from database.engine_session_initialization import Session


class WarcraftCharactersDatabaseMethods:
    @classmethod
    async def character_exists(cls, name: str, realm: str):
        session = Session()
        results = session.query(Character).filter_by(
            name=name.lower(), realm=realm.replace(' ', '-').lower()).first()
        if results is None:
            return False
        return True

    @classmethod
    async def create_new_character(cls, raiderio_data: dict, blizzard_data: dict, honor_level: int,
                                   rank: str=None):
        session = Session()
        new_character = Character()
        new_character.name = raiderio_data['name'].lower()
        new_character.realm = raiderio_data['realm'].replace(' ', '-').lower()
        new_character.region = raiderio_data['region'].lower()
        if 'guild' in blizzard_data.keys():
            new_character.guild = blizzard_data['guild']['name']
        else:
            new_character.guild = ''
        if rank is not None:
            new_character.guild_rank = rank
        new_character.char_class = raiderio_data['class'].lower()
        new_character.ilvl = blizzard_data['items']['averageItemLevelEquipped']
        new_character.heart_of_azeroth_level = blizzard_data['items']['neck']['azeriteItem']['azeriteLevel']
        new_character.m_plus_score_overall = raiderio_data['mythic_plus_scores']['all']
        new_character.m_plus_rank_overall = raiderio_data['mythic_plus_ranks']['overall']['realm']
        new_character.m_plus_rank_class = raiderio_data['mythic_plus_ranks']['class']['realm']
        if len(raiderio_data['mythic_plus_highest_level_runs']) != 0:
            if len(raiderio_data['mythic_plus_weekly_highest_level_runs']) != 0:
                new_character.m_plus_weekly_high = raiderio_data['mythic_plus_weekly_highest_level_runs'][0]['mythic_level']
            else:
                new_character.m_plus_weekly_high = 0
        else:
            new_character.m_plus_weekly_high = 0
        new_character.honor_level = honor_level
        new_character.last_updated = datetime.datetime.now()
        session.add(new_character)
        session.commit()

    @classmethod
    async def update_character(cls, raiderio_data: dict, blizzard_data: dict, honor_level: int,
                               rank: str=None):
        session = Session()
        character = session.query(Character).filter_by(
            name=raiderio_data['name'].lower(),
            realm=raiderio_data['realm'].replace(' ', '-').lower()).first()
        if 'guild' in blizzard_data.keys():
            character.guild = blizzard_data['guild']['name']
        else:
            character.guild = ''
        if rank is not None:
            character.guild_rank = rank
        character.char_class = raiderio_data['class'].lower()
        character.ilvl = blizzard_data['items']['averageItemLevelEquipped']
        character.heart_of_azeroth_level = blizzard_data['items']['neck']['azeriteItem']['azeriteLevel']
        character.m_plus_score_overall = raiderio_data['mythic_plus_scores']['all']
        character.m_plus_rank_overall = raiderio_data['mythic_plus_ranks']['overall']['realm']
        character.m_plus_rank_class = raiderio_data['mythic_plus_ranks']['class']['realm']
        if len(raiderio_data['mythic_plus_highest_level_runs']) != 0:
            if len(raiderio_data['mythic_plus_weekly_highest_level_runs']) != 0:
                character.m_plus_weekly_high = raiderio_data['mythic_plus_weekly_highest_level_runs'][0]['mythic_level']
            else:
                character.m_plus_weekly_high = 0
        else:
            character.m_plus_weekly_high = 0
        character.honor_level = honor_level
        character.last_updated = datetime.datetime.now()
        session.add(character)
        session.commit()

    @classmethod
    async def claim_character(cls, name: str, realm: str, guild_id: int):
        session = Session()
        character = session.query(Character).filter_by(
            name=name.lower(), realm=realm.replace(' ', '-').lower()).first()
        character.claimed_on = guild_id
        session.add(character)
        session.commit()

    @classmethod
    async def unclaim_character(cls, name: str, realm: str, guild_id: int):
        session = Session()
        character = session.query(Character).filter_by(
            name=name.lower(), realm=realm.replace(' ', '-').lower()).first()
        character.claimed_on = guild_id
        session.delete(character)
        session.commit()

    @classmethod
    async def get_claimed_characters(cls, guild_id: int):
        session = Session()
        results = session.query(Character).filter_by(
            claimed_on=guild_id).all()
        return results

    @classmethod
    async def get_scores(cls, guild_id: int):
        session = Session()
        results = session.query(Character).filter_by(claimed_on=guild_id).filter(
            Character.m_plus_score_overall > 0).order_by(
            desc(Character.m_plus_score_overall)).order_by(
            asc(Character.name)).all()
        return results

    @classmethod
    async def get_honor_levels(cls, guild_id: int):
        session = Session()
        results = session.query(Character).filter_by(claimed_on=guild_id).filter(
            Character.honor_level > 0).order_by(
            desc(Character.honor_level)).order_by(
            asc(Character.name)).all()
        return results

    @classmethod
    async def get_raiders(cls, guild_id: int, ranks: list, sort_method: str='rank'):
        session = Session()
        if sort_method == 'rank':
            results = session.query(Character).filter_by(claimed_on=guild_id).filter(
                Character.guild_rank.in_(ranks)).order_by(asc(Character.guild_rank)).order_by(
                Character.name).all()
            return results
        if sort_method == 'class':
            results = session.query(Character).filter_by(claimed_on=guild_id).filter(
                Character.guild_rank.in_(ranks)).order_by(asc(Character.char_class)).order_by(
                Character.name).all()
            return results
        if sort_method == 'ilvl':
            results = session.query(Character).filter_by(claimed_on=guild_id).filter(
                Character.guild_rank.in_(ranks)).order_by(desc(Character.ilvl)).order_by(
                Character.name).all()
            return results
        if sort_method == 'mplus':
            results = session.query(Character).filter_by(claimed_on=guild_id).filter(
                Character.guild_rank.in_(ranks)).order_by(desc(Character.m_plus_weekly_high)).order_by(
                Character.name).all()
            return results
        if sort_method == 'hoa':
            results = session.query(Character).filter_by(claimed_on=guild_id).filter(
                Character.guild_rank.in_(ranks)).order_by(desc(Character.heart_of_azeroth_level)).order_by(
                Character.name).all()
            return results

    @classmethod
    async def add_key(cls, name: str, dungeon: str, level: int):
        session = Session()
        character = session.query(Character).filter_by(name=name.lower()).first()
        character.m_plus_key = dungeon
        character.m_plus_key_level = level
        session.add(character)
        session.commit()

    @classmethod
    async def remove_key(cls, name: str):
        session = Session()
        character = session.query(Character).filter_by(name=name.lower()).first()
        character.m_plus_key = None
        character.m_plus_key_level = None
        session.add(character)
        session.commit()

    @classmethod
    async def reset_keys(cls):
        session = Session()
        characters = session.query(Character).filter(Character.m_plus_key is not None).all()
        for char in characters:
            char.m_plus_key = None
            char.m_plus_key_level = None
            session.add(char)
        session.commit()

    @classmethod
    async def get_keys(cls, guild_id: int):
        session = Session()
        results = session.query(Character).filter_by(
            claimed_on=guild_id).filter(Character.m_plus_key_level > 1).order_by(
            desc(Character.m_plus_key_level)).order_by(asc(Character.name)).all()
        return results