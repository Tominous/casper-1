import datetime

from database.database_models import Bans
from database.engine_session_initialization import Session


class BanMethods:
    @classmethod
    async def user_is_banned(cls, user: str):
        session = Session()
        results = session.query(Bans).filter_by(user=user).first()
        if results is None:
            return False
        return True

    @classmethod
    async def ban_user(cls, user: str, banned_by: str, ban_reason, ban_time):
        session = Session()
        ban = session.query(Bans).filter_by(user=user).first()
        if ban is None:
            ban = Bans()
        ban.user = user
        ban.banned_by = banned_by.lower()
        ban.ban_reason = ban_reason
        ban.banned_on = datetime.datetime.now()
        ban.ban_time = ban_time
        session.add(ban)
        session.commit()
        return

    @classmethod
    async def unban_user(cls, user: str):
        session = Session()
        ban = session.query(Bans).filter_by(user=user).first()
        session.delete(ban)
        session.commit()
        return

    @classmethod
    async def get_ban_list(cls):
        session = Session()
        bans = session.query(Bans).all()
        return bans
