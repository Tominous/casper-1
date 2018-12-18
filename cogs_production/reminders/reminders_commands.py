"""
Author:         David Schaeffer
Creation Date:  December 13, 2018
Purpose:        Defines all commands for the Reminder module
"""
import asyncio
import datetime

from discord.ext import commands
from database.database import RemindersDatabaseMethods


class Reminder:
    def __init__(self, casper):
        self.casper = casper
        self.casper.loop.create_task(self.get_reminders())

    async def get_reminders(self):
        """
        Checks for new reminders every 60 seconds for every server the bot belongs to.
        :return: None
        """
        await self.casper.wait_until_ready()
        while not self.casper.is_closed():
            guilds = self.casper.guilds
            for guild in guilds:
                reminders = await RemindersDatabaseMethods.get_reminders(guild.id)
                if len(reminders) != 0:
                    for reminder in reminders:
                        ch = self.casper.get_channel(reminder.channel)
                        await ch.send(
                            f'{reminder.user}, I\'m reminding you about:\n'
                            f'{reminder.message}')
                        await RemindersDatabaseMethods.remove_reminder(reminder.id)
            await asyncio.sleep(60)

    @commands.command()
    async def remindme(self, ctx, *, rest: str):
        """
        Accepts minutes, hours, days, weeks, months, and years.
        Ex: casper remindme 6 days Check out the new movie.
        """
        # current_date = datetime.date.today()
        # print(current_date)
        current_time = datetime.datetime.today()
        try:
            # Coercing the time to an int is an easy way to ensure data coming in is in
            # proper order.
            count = int(rest.split(' ')[0])
        except ValueError:
            return await ctx.send('You need to use a valid integer time frame.\n'
                                  'Ex: 1 day, 3 months, 10 years')
        when = rest.split(' ')[1]
        if 'min' in when:
            reminder_time = current_time + datetime.timedelta(minutes=count)
        elif 'hour' in when or 'hrs' in when:
            reminder_time = current_time + datetime.timedelta(hours=count)
        elif 'day' in when:
            reminder_time = current_time + datetime.timedelta(days=count)
        elif 'week' in when:
            reminder_time = current_time + datetime.timedelta(hours=(count*7)*24)
        elif 'month' in when or 'mos' in when:
            reminder_time = current_time + datetime.timedelta(days=(count*30))
        elif 'year' in when or 'yrs' in when:
            reminder_time = current_time + datetime.timedelta(days=(count*365))
        else:
            return await ctx.send('I did not recognize that time frame. Sorry.\n'
                                  'Ex: 1 day, 3 months, 10 years')
        # Grabs just the bit of the message that needs to be used as the reminder.
        reminder_msg = ' '.join(rest.split(' ')[2:])
        await RemindersDatabaseMethods.add_reminder(ctx.guild.id, ctx.author.mention,
                                                    reminder_msg, ctx.channel.id,
                                                    reminder_time)
        return await ctx.send(f'I will be reminding you about:\n{reminder_msg}\non\n'
                              f'{reminder_time}.')


def setup(casper):
    casper.add_cog(Reminder(casper))
