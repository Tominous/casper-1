"""
Author:         David Schaeffer
Creation Date:  December 13, 2018
Purpose:        Defines all commands for the Reminder module
"""
import asyncio
import datetime

from discord.ext import commands
from database.reminders import RemindersDatabaseMethods
from database.countdownevents import CountdownEventsDatabaseMethods


class Reminder:
    def __init__(self, casper):
        self.casper = casper
        self.casper.loop.create_task(self.get_reminders())

    async def get_reminders(self):
        """
        Checks for new reminders every 60 seconds for every server the casper belongs to.
        :return: None
        """
        await self.casper.wait_until_ready()
        while not self.casper.is_closed():
            guilds = self.casper.guilds
            for guild in guilds:
                reminders = await RemindersDatabaseMethods.auto_get_reminders(guild.id)
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

    @commands.command()
    async def addevent(self, ctx, event_date: str, *, event_name: str):
        """
        Add an event to be tracked by the countdown command.
        :param ctx: Invoked context.
        :param event_date: Date of the event.
        :param event_name: Name of the event.
        :return: On successful event creation, confirmation message. Else, usage message.
        """
        usage_msg = ('Please format your date as MM/DD/YYYY.\n'
                     'Ex: casper addevent 01/01/2019 Happy New Year!')
        if '/' not in event_date:
            return await ctx.send(usage_msg)
        try:
            month, day, year = event_date.split('/')
            month = int(month)
            day = int(day)
            year = int(year)
        except ValueError:
            return await ctx.send(usage_msg)
        if 0 < month < 13 and 0 < day < 32 and 0 < year < 100000:
            event_date = datetime.date(year, month, day)
            await CountdownEventsDatabaseMethods.add_event(
                ctx.guild.id, event_name, event_date)
            return await ctx.send(f'Countdown for {event_name} on {event_date} created.')
        else:
            return await ctx.send(usage_msg)

    @commands.command()
    async def removeevent(self, ctx, event_date: str, *, event_name: str):
        """
        Removes an event from the countdown tracker.
        :param ctx: Invoked context.
        :param event_date: Date of the event.
        :param event_name: Name of the event.
        :return: On successful event deletion, confirmation message. Else, error message.
        """
        usage_msg = ('Please format your date as MM/DD/YYYY.\n'
                     'Ex: casper removeevent 01/01/2019 Happy New Year!')
        if '/' not in event_date:
            return await ctx.send(usage_msg)
        try:
            month, day, year = event_date.split('/')
            month = int(month)
            day = int(day)
            year = int(year)
        except ValueError:
            return await ctx.send(usage_msg)
        if 0 < month < 13 and 0 < day < 32 and 0 < year < 100000:
            event_date = datetime.date(year, month, day)
            if await CountdownEventsDatabaseMethods.remove_event(
                    ctx.guild.id, event_name, event_date):
                return await ctx.send(f'Countdown for {event_name} on {event_date} '
                                      f'removed.')
            else:
                return await ctx.send(f'Could not find event matching "{event_name}" on '
                                      f'{event_date}. To delete an event, you must make '
                                      f'sure the date and name match **__exactly__**.')
        else:
            return await ctx.send(usage_msg)

    @commands.command()
    async def countdown(self, ctx, *, event_name: str=None):
        """
        Get the current countdown to a given event, or all events if no event name is
        given.
        :param ctx: Invoked context.
        :param event_name: Name of the event to countdown to.
        :return: If event_name is given, all events which match. Else, every event for
            the particular discord server.
        """
        if event_name:
            events = await CountdownEventsDatabaseMethods.get_event(
                ctx.guild.id, event_name)
        else:
            events = await CountdownEventsDatabaseMethods.get_all_events(ctx.guild.id)
        if events:
            output_str = ''
            for event in events:
                days_til_event = (event.event_date - datetime.date.today()).days
                if days_til_event < 0:
                    await CountdownEventsDatabaseMethods.auto_remove_event(ctx.guild.id,
                                                                           event.id)
                    output_str += (f'The event "{event.event_name}" has passed and '
                                   f'has been removed from the countdown tracker.\n')
                    continue
                output_str += (f'There are {days_til_event} days left until '
                               f'{event.event_name}.\n\n')
            return await ctx.send(output_str)
        else:
            return await ctx.send('Could not find any events for this server matching '
                                  'your query.')


def setup(casper):
    casper.add_cog(Reminder(casper))
