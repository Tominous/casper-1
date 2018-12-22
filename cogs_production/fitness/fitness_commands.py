"""
Author:         David Schaeffer
Creation Date:  November 6, 2018
Purpose:        Defines all commands for the Fitness module
"""
import decimal

from discord.ext import commands
from database.database import FitnessDatabaseMethods


class Fitness:
    def __init__(self, casper):
        self.casper = casper

    @staticmethod
    async def calc_wilks(gender, bodyweight, bench, squat, dead):
        # test values
        bodyweight = decimal.Decimal('81.6466')
        total = decimal.Decimal('474.004')
        kg_constant = decimal.Decimal('2.205')
        x = bodyweight
        am = decimal.Decimal('-216.0475144')
        bm = decimal.Decimal('16.2606339')
        cm = decimal.Decimal('-0.002388645')
        dm = decimal.Decimal('-0.00113732')
        em = decimal.Decimal('0.00000701863')
        fm = decimal.Decimal('-0.00000001291')
        af = decimal.Decimal('594.31747775582')
        bf = decimal.Decimal('-27.23842536447')
        cf = decimal.Decimal('0.82112226871')
        df = decimal.Decimal('-0.00930733913')
        ef = decimal.Decimal('0.00004731582')
        ff = decimal.Decimal('-0.00000009054')
        coeff_m = 500 / (
            am + (bm * x) + (cm * (x ** 2)) + (dm * (x ** 3)) + (em * (x ** 4)) + (fm * (x ** 5))
        )
        coeff_f = 500 / (
            af + (bf * x) + (cf * (x ** 2)) + (df * (x ** 3)) + (ef * (x ** 4)) + (ff * (x ** 5))
        )
        return total * coeff_m

    @commands.command()
    async def setgender(self, ctx, gender):
        await FitnessDatabaseMethods.setgender(ctx.author.name, ctx.guild.id, gender)
        return await ctx.send(f'Gender set for {ctx.author.name.title()}.')

    @commands.command()
    async def setheight(self, ctx, height):
        try:
            await FitnessDatabaseMethods.setheight(ctx.author.name, ctx.guild.id, float(height))
            return await ctx.send(f'Height set for {ctx.author.name.title()}.')
        except ValueError:
            return await ctx.send('Please enter your height in inches.')

    @commands.command()
    async def setweight(self, ctx, weight):
        try:
            await FitnessDatabaseMethods.setweight(ctx.author.name, ctx.guild.id, float(weight))
            return await ctx.send(f'Weight set for {ctx.author.name.title()}.')
        except ValueError:
            return await ctx.send('Please enter your weight in pounds.')

    @commands.command()
    async def setbench(self, ctx, weight):
        try:
            await FitnessDatabaseMethods.setbench(ctx.author.name, ctx.guild.id, float(weight))
            return await ctx.send(f'Flat bench weight set for {ctx.author.name.title()}.')
        except ValueError:
            return await ctx.send('Please enter your weight in pounds.')

    @commands.command()
    async def setsquat(self, ctx, weight):
        try:
            await FitnessDatabaseMethods.setsquat(ctx.author.name, ctx.guild.id, float(weight))
            return await ctx.send(f'Back squat weight set for {ctx.author.name.title()}.')
        except ValueError:
            return await ctx.send('Please enter your weight in pounds.')

    @commands.command()
    async def setdeadlift(self, ctx, weight):
        try:
            await FitnessDatabaseMethods.setdeadlift(ctx.author.name, ctx.guild.id, float(weight))
            return await ctx.send(f'Deadlift weight set for {ctx.author.name.title()}.')
        except ValueError:
            return await ctx.send('Please enter your weight in pounds.')

    @commands.command()
    async def setohp(self, ctx, weight):
        try:
            await FitnessDatabaseMethods.setohp(ctx.author.name, ctx.guild.id, float(weight))
            return await ctx.send(f'OHP weight set for {ctx.author.name.title()}.')
        except ValueError:
            return await ctx.send('Please enter your weight in pounds.')

    @commands.command()
    async def setmile(self, ctx, time):
        if ':' not in time:
            return await ctx.send('Please enter your time as `M:SS`.')
        await FitnessDatabaseMethods.setmile(ctx.author.name, ctx.guild.id, time)
        return await ctx.send(f'Run 1 mile time set for {ctx.author.name.title()}.')

    @commands.command()
    async def setrowing(self, ctx, time):
        if ':' not in time:
            return await ctx.send('Please enter your time as `M:SS`.')
        await FitnessDatabaseMethods.setrowing(ctx.author.name, ctx.guild.id, time)
        return await ctx.send(f'2000 meter row time set for {ctx.author.name.title()}.')

    @commands.command()
    async def setburpees(self, ctx, count):
        try:
            await FitnessDatabaseMethods.setburpees(ctx.author.name, ctx.guild.id, int(count))
            return await ctx.send(f'Number of burpess in 1 minute set for '
                                  f'{ctx.author.name.title()}.')
        except ValueError:
            return await ctx.send('Please enter the number of burpees as a whole number.')

    @commands.command()
    async def setplank(self, ctx, time):
        if ':' not in time:
            return await ctx.send('Please enter your time as `M:SS`.')
        await FitnessDatabaseMethods.setplank(ctx.author.name, ctx.guild.id, time)
        return await ctx.send(f'Plank time set for {ctx.author.name.title()}.')

    @commands.command()
    async def progress(self, ctx, user=None):
        """Check the current progress of someone."""
        if user is None:
            user = ctx.author.name
        else:
            guild_users = [name.name.lower() for name in self.casper.users]
            if user in guild_users:
                pass
            else:
                return await ctx.send('Could not find that user.')
        fitness_user = await FitnessDatabaseMethods.get_progress(user, ctx.guild.id)
        output_str = f'**__Current Progress for {fitness_user.user.title()}:__**\n'
        try:
            output_str += (f'{fitness_user.gender.title()} / {fitness_user.height} in. / '
                           f'{fitness_user.weight} lbs\n\n'
                           f'Bench: {fitness_user.bench_press} lbs **|** '
                           f'Squat: {fitness_user.back_squat} lbs **|** '
                           f'Deadlift: {fitness_user.deadlift} lbs **|** '
                           f'OHP: {fitness_user.ohp} lbs\n\n'
                           f'Mile Run Time: {fitness_user.mile} **|** '
                           f'2000 Meter Row Time: {fitness_user.row_2km}\n\n'
                           f'Burpees in 1 min: {fitness_user.burpess_1m} **|** '
                           f'Plank time: {fitness_user.plank}')
        except AttributeError:
            output_str += f'{fitness_user.user.title()} has not entered any info yet.'
        return await ctx.send(output_str)


def setup(casper):
    casper.add_cog(Fitness(casper))
