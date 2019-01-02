"""
Author:         David Schaeffer
Creation Date:  November 6, 2018
Purpose:        Defines all commands for the Dice module
"""

import random
import re

from discord.ext import commands


class Dice:
    def __init__(self, casper):
        self.casper = casper

    @commands.command()
    async def roll(self, ctx, *, text):
        """
        Enter a single number as the 1-? limit: 20, or a string: 2d10+1d6+4+1d4-2d4-8+1d4-1d4
        """
        # d in text means we're rolling some bones!
        if 'd' in text:  # 2d10+1d6+4+1d4-2d4-8+1d4-1d4
            total = 0
            # This is a large try/except block, but it made sense since I don't return
            # specific messages for the same exception. If the user enters a non-int when
            # an int is expected, or they add a character that breaks our splitting and
            # parsing of the text, they get an error message. Ex: \, g, *, etc
            try:
                # Match any NdNN not preceeded by a -
                positive_dice_rolls_regex = re.compile(r'((?<!-)\dd\d*)')
                match = positive_dice_rolls_regex.findall(text)
                if match:
                    # list of NdNN
                    # print(f'match for pos: {match}')
                    for roll in match:
                        num_dice, die_size = roll.split('d')
                        # Add the results to the total
                        total += await self.get_roll_result(int(num_dice), int(die_size))

                # Match any NdNN not preceeded by a +
                negative_dice_rolls_regex = re.compile(r'([^\s](?<!\+)\dd\d*)')
                match = negative_dice_rolls_regex.findall(text)
                if match:
                    # list of NdNN
                    # print(f'match for neg: {match}')
                    for roll in match:
                        num_dice, die_size = roll.replace('-', '').split('d')
                        # Subtract the results from the total
                        total -= await self.get_roll_result(int(num_dice), int(die_size))

                # Match any +N modifiers
                postive_modifiers_regex = re.compile(r'\+(\d)[\+|-]')
                match = postive_modifiers_regex.findall(text)
                if match:
                    # list of N
                    # print(f'match for pos mods: {match}')
                    for mod in match:
                        # Add mod to total
                        total += int(mod)

                # Match any -N modifiers
                negative_modifiers_regex = re.compile(r'-(\d)[\+|-]')
                match = negative_modifiers_regex.findall(text)
                if match:
                    # list of N
                    # print(f'match for neg mods: {match}')
                    for mod in match:
                        # Subtract mod from total
                        total -= int(mod)
            except ValueError:
                return await ctx.send('Looks like you have mistyped a number in there '
                                      'somewhere.')
            # print(f'Total: {total}')
            return await ctx.send(f'Your total is: {total}')
        else:
            return await ctx.send(random.randint(1, int(text)))

    @staticmethod
    async def get_roll_result(num_dice, die_size):
        result = 0
        while num_dice > 0:
            r = random.randint(1, die_size)
            # print(f'roll: {r}')
            result += r
            num_dice -= 1
        # print(f'result: {result}')
        return result


def setup(casper):
    casper.add_cog(Dice(casper))
