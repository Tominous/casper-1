from datetime import datetime

from database.database_models import Reminders
from database.engine_session_initialization import Session


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
    async def auto_get_reminders(cls, guild_id: int):
        session = Session()
        # Reminders.when < datetime.today() because we don't actually fetch the reminder
        # until the next minute-interval check following the reminder time.
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