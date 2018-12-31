from datetime import date

from sqlalchemy import asc

from database.database_models import CountdownEvents
from database.engine_session_initialization import Session


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
    async def auto_remove_event(cls, guild_id: int, event_id):
        session = Session()
        event = session.query(CountdownEvents).filter_by(id=event_id,
                                                         guild_id=guild_id).first()
        session.delete(event)
        session.commit()
        session.close()

    @classmethod
    async def remove_event(cls, guild_id: int, event_name: str, event_date: date):
        session = Session()
        event = session.query(CountdownEvents).filter_by(
            guild_id=guild_id, event_name=event_name, event_date=event_date).first()
        if event is not None:
            session.delete(event)
            session.commit()
            session.close()
            return True
        return False

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