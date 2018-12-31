from database.database_models import Fitness
from database.engine_session_initialization import Session


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