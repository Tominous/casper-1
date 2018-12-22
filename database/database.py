from datetime import date, datetime

from sqlalchemy import desc, asc

from database.engine_session_initialization import Session
from database.database_models import Character, Fitness, CountdownEvents, Reminders


class CharactersDatabaseMethods:
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
        character.last_updated = date.today()
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
                desc(Character.ilvl)).all()
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


class FitnessDatabaseMethods:
    @classmethod
    async def get_user(cls, user, guild_id: int):
        """
        Checks to see if a user exists already. If not, it creates a new record. Returns
        user record.
        :param user: the user to fetch
        :param guild_id: the id of the discord server the user belongs to
        :return: the user record
        """
        session = Session()
        fitness = session.query(Fitness).filter_by(user=user.lower(),
                                                   guild_id=guild_id).first()
        if fitness is None:
            fitness = Fitness()
            fitness.user = user.lower()
            fitness.guild_id = guild_id
            session.close()
            return fitness
        session.close()
        return fitness

    @classmethod
    async def setgender(cls, user, guild_id: int, gender: str):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.gender = gender.lower()
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setheight(cls, user, guild_id: int, height: float):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.height = height
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setweight(cls, user, guild_id: int, weight: float):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.weight = weight
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setbench(cls, user, guild_id: int, weight: float):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.bench_press = weight
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setsquat(cls, user, guild_id: int, weight: float):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.back_squat = weight
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setdeadlift(cls, user, guild_id: int, weight: float):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.deadlift = weight
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setohp(cls, user, guild_id: int, weight: float):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.ohp = weight
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setmile(cls, user, guild_id: int, time: str):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.mile = time
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setrowing(cls, user, guild_id: int, time: str):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.row_2km = time
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setburpees(cls, user, guild_id: int, count: int):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.burpess_1m = count
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def setplank(cls, user, guild_id: int, time: str):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        fitness.plank = time
        session.add(fitness)
        session.commit()
        session.close()

    @classmethod
    async def get_progress(cls, user, guild_id: int):
        session = Session()
        fitness = await cls.get_user(user.lower(), guild_id)
        session.add(fitness)
        session.commit()
        return fitness


class CountdownEventsDatabaseMethods:
    @classmethod
    async def add_event(cls, guild_id: int, event_name: str, event_date: date):
        session = Session()
        event = CountdownEvents()
        event.guild_id = guild_id
        event.event_name = event_name
        event.event_date = event_date
        session.add(event)
        session.commit()
        session.close()

    @classmethod
    async def remove_event(cls, guild_id: int, event_id):
        session = Session()
        event = session.query(CountdownEvents).filter_by(id=event_id,
                                                         guild_id=guild_id).first()
        session.delete(event)
        session.commit()
        session.close()

    @classmethod
    async def get_event(cls, guild_id: int, event_name: str):
        session = Session()
        event = session.query(CountdownEvents).filter_by(guild_id=guild_id).filter(
            CountdownEvents.event_name.ilike(f'%{event_name}%')).order_by(
            asc(CountdownEvents.event_date)).all()
        return event

    @classmethod
    async def get_all_events(cls, guild_id: int):
        session = Session()
        events = session.query(CountdownEvents).filter_by(guild_id=guild_id).all()
        return events


class RemindersDatabaseMethods:
    @classmethod
    async def add_reminder(cls, guild_id, user, reminder_msg, channel, reminder_time):
        session = Session()
        reminder = Reminders()
        reminder.guild_id = guild_id
        reminder.user = user
        reminder.message = reminder_msg
        reminder.channel = channel
        reminder.when = reminder_time
        session.add(reminder)
        session.commit()
        session.close()

    @classmethod
    async def get_reminders(cls, guild_id):
        session = Session()
        results = session.query(Reminders).filter_by(guild_id=guild_id).filter(
            Reminders.when < datetime.today()).all()
        return results

    @classmethod
    async def remove_reminder(cls, reminder_id):
        session = Session()
        reminder = session.query(Reminders).filter_by(id=reminder_id).first()
        session.delete(reminder)
        session.commit()
        session.close()
