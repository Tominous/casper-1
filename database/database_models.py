from datetime import date

from sqlalchemy import Column, Date, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from database.engine_session_initialization import engine


Base = declarative_base()


class Character(Base):
    __tablename__ = 'characters'
    name = Column(String, primary_key=True)
    realm = Column(String, primary_key=True)
    region = Column(String)
    guild = Column(String)
    guild_rank = Column(Integer)
    claimed_on = Column(Integer)
    char_class = Column(String)
    ilvl = Column(Integer)
    heart_of_azeroth_level = Column(Integer)
    m_plus_key = Column(String)
    m_plus_key_level = Column(Integer)
    m_plus_highest_score = Column(Integer)
    m_plus_score_overall = Column(Integer)
    m_plus_rank_overall = Column(Integer)
    m_plus_rank_class = Column(Integer)
    m_plus_weekly_high = Column(Integer)
    honor_level = Column(Integer)
    last_updated = Column(DateTime)

    def __repr__(self):
        return (f'<Character('
                f'name={self.name}, '
                f'realm={self.realm}, '
                f'region={self.region}, '
                f'claimed_on={self.claimed_on}, '
                f'char_class={self.char_class}, '
                f'm_plus_key={self.m_plus_key}, '
                f'm_plus_key_level={self.m_plus_key_level}, '
                f'm_plus_score_overall={self.m_plus_score_overall}, '
                f'm_plus_rank_overall={self.m_plus_rank_overall}, '
                f'm_plus_rank_class={self.m_plus_rank_class}, '
                f'honor_level={self.honor_level})>\n\n')


class Fitness(Base):
    __tablename__ = 'fitness'
    user = Column(String, primary_key=True)
    guild_id = Column(String, primary_key=True)
    gender = Column(String)
    height = Column(Float)
    weight = Column(Float)
    bench_press = Column(Float)
    back_squat = Column(Float)
    deadlift = Column(Float)
    ohp = Column(Float)
    wilks = Column(Float)
    mile = Column(String)
    row_2km = Column(String)
    burpess_1m = Column(Integer)
    plank = Column(String)
    goal_weight = Column(Float)

    def __repr__(self):
        return (f'<FitnessUser('
                f'name={self.user},'
                f'guild={self.guild_id})>')


class CountdownEvents(Base):
    __tablename__ = 'countdownevents'
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    event_name = Column(String)
    event_date = Column(Date)


class Reminders(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    user = Column(String)
    message = Column(String)
    channel = Column(Integer)
    when = Column(DateTime)


class Bans(Base):
    __tablename__ = 'bans'
    user = Column(String, primary_key=True)
    banned_by = Column(String)
    ban_reason = Column(String)
    banned_on = Column(DateTime)
    ban_time = Column(Integer)  # Hours


Base.metadata.create_all(engine)
