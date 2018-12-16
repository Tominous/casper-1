"""
Author:         David Schaeffer
Creation Date:  November 6, 2018
Purpose:        Defines all commands for the Dice module
"""

import random

from discord.ext import commands


class Dice:
    def __init__(self, casper):
        self.casper = casper

    @commands.command()
    async def roll(self, ctx, *, text):
        """
        Enter a single number as the 1-? limit or a string: 2d10+1d6+4+1d4-2
        """
        if 'd' in text:  # 2d10+1d6+4+1d4-2
            result = 0
            pos_rolls = text.split('+')
            print(f'pos_rolls = {pos_rolls}')
            for roll in pos_rolls:
                print(f'roll in pos_rolls = {roll}')
                if 'd' in roll:
                    if '-' in roll:
                        sub_rolls = roll.split('-')
                        print(f'sub_rolls = {sub_rolls}')
                        for sub_roll in sub_rolls:
                            print(f'sub_roll in sub_rolls = {sub_roll}')
                            if 'd' in sub_roll:
                                num_dice, die_size = sub_roll.split('d')
                                for j in range(int(num_dice)):
                                    result += random.randint(1, int(die_size))
                            else:
                                result -= int(sub_roll)
                    else:
                        num_dice, die_size = roll.split('d')
                        for i in range(int(num_dice)):
                            result += random.randint(1, int(die_size))
                else:
                    if '-' in roll:  # +4-2
                        add_r, minus_r = roll.split('-')
                        result += int(add_r)
                        result -= int(minus_r)
                    else:  # +2
                        result += int(roll)
            return await ctx.send(result)
        return await ctx.send(random.randint(1, int(text)))


def setup(casper):
    casper.add_cog(Dice(casper))
