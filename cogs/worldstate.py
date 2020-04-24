# Cog for handling Warframe worldstate
# Uses data from the warframestat.us API
# Documentation: docs.warframestat.us

import discord
from discord.ext import commands
import json
import requests
from datetime import datetime
import dateutil.parser, dateutil.relativedelta
import traceback
from .utils import wfpics

class Worldstate(commands.Cog):
    #initizes client
    def _init_(self, client):
        self.client = client

    #tells when it is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded cog: WF Worldstate (cogs/worldstate.py)')

    # ~worldstate subcommands, for testing use
    @commands.group(aliases=['ws'], help='Information about Warframe\'s world state')
    async def worldstate(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid world state command')

    @worldstate.command(name='ping', help='Ping the world state api to check that it\'s still online and working properly')
    async def ping(self, ctx):
        request = requests.get('https://api.warframestat.us/pc')
        request.raise_for_status()
        response = request.json()
        await ctx.send(f"World state is live as of {response['timestamp']}")

    # The rest of these commands don't require a prefix


    # Checks current cycles for the two open worlds (PoE and Vallis)
    @commands.command(name='cycle', aliases=['ow'], help='Checks the cycles of the two open worlds')
    async def cycle(self, ctx):
        cetusRequest = requests.get('https://api.warframestat.us/pc/cetusCycle')
        cetusRequest.raise_for_status()
        cetusResponse = cetusRequest.json()

        vallisRequest = requests.get('https://api.warframestat.us/pc/vallisCycle')
        vallisRequest.raise_for_status()
        vallisResponse = vallisRequest.json()

        embed = discord.Embed(title="Open World Cycles", colour=discord.Colour(0x4eb31c))
        embed.add_field(name="Plains of Eidolon", value=f"**{cetusResponse['state'].title()}** ({cetusResponse['shortString']})", inline=True)
        embed.add_field(name="Orb Vallis", value=f"**{vallisResponse['state'].title()}** ({vallisResponse['shortString']})", inline=True)
        embed.set_footer(text=f"Last updated {datetime.now().strftime('%m/%d/%Y %H:%M')}")
        await ctx.send(embed=embed)

    # Checks current weekly nightwave challenges (dailies not counted)
    @commands.command(name='nightwave', aliases=['nw'], help='Check this week\'s nightwave challenges')
    async def nightwave(self, ctx):
        try:
            request = requests.get('https://api.warframestat.us/pc/nightwave')
            request.raise_for_status()
            response = request.json()

            nw_current_season = response["season"]
            nw_weekly_normal_challenges = [c for c in response['activeChallenges'] if c['active'] and 'isDaily' not in c and not c['isElite']]
            nw_weekly_elite_challenges = [c for c in response['activeChallenges'] if c['active'] and 'isDaily' not in c and c['isElite']]
            nw_current_week = dateutil.parser.parse(nw_weekly_normal_challenges[0]["activation"])
            nw_current_expiry = dateutil.parser.parse(nw_weekly_normal_challenges[0]["expiry"])
            nw_current_time_delta = dateutil.relativedelta.relativedelta(nw_current_expiry.replace(tzinfo=None), datetime.utcnow())

            embed = discord.Embed(title=f"Nightwave Season {nw_current_season}",
                                  colour=discord.Colour(0x4eb31c),
                                  description=f"Week of {nw_current_week.strftime('%B %d')}, ends in {nw_current_time_delta.days}d{nw_current_time_delta.hours}h")
            embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/warframe/images/9/95/Nora_Night_transmission.png")
            nw_weekly_normal_challenges_string = ""
            for challenge in nw_weekly_normal_challenges:
                nw_weekly_normal_challenges_string += f"**{challenge['title']}**\n{challenge['desc']}\n\n"
            nw_weekly_elite_challenges_string = ""
            for challenge in nw_weekly_elite_challenges:
                nw_weekly_elite_challenges_string += f"**{challenge['title']}**\n{challenge['desc']}\n\n"
            embed.add_field(name=f"Weekly Challenges ({nw_weekly_normal_challenges[0]['reputation']} reputation each)",
                            value=nw_weekly_normal_challenges_string,
                            inline=False)
            embed.add_field(name=f"Elite Weekly Challenges ({nw_weekly_elite_challenges[0]['reputation']} reputation each)",
                            value=nw_weekly_elite_challenges_string,
                            inline=False)
            embed.set_footer(text=f"Last updated {datetime.now().strftime('%m/%d/%Y %H:%M')}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"🛑 An error occured! 🛑 \n```{traceback.format_exc()}```")


    # Checks current fissures and their time remaining
    @commands.command(name='fissures', aliases=['fis'], help='Gives information about active void fissures')
    async def fissures(self, ctx):
        try:
            request = requests.get('https://api.warframestat.us/pc/fissures')
            request.raise_for_status()
            response = request.json()

            divided_fissures_list = []
            for tier in (1, 2, 3, 4, 5):
                divided_fissures_list.append([fis for fis in response if fis['tierNum'] == tier and fis['active'] and not fis['expired']])

            fissures_strings = []
            for fissures in divided_fissures_list:
                fissure_string = ""
                for fis in fissures:
                    fissure_string += f"**{fis['node']}** -  {fis['missionType']} *({fis['eta']} left)*\n"
                fissures_strings.append(fissure_string)

            embed = discord.Embed(title=f"Active Void Fissures",
                                  colour=discord.Colour(0x4eb31c))
            embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/warframe/images/5/57/VoidTearIcon_b.png")
            embed.add_field(name=f"Lith Fissures", value=fissures_strings[0], inline=False)
            embed.add_field(name=f"Meso Fissures", value=fissures_strings[1], inline=False)
            embed.add_field(name=f"Neo Fissures", value=fissures_strings[2], inline=False)
            embed.add_field(name=f"Axi Fissures", value=fissures_strings[3], inline=False)
            embed.add_field(name=f"Requiem Fissures", value=fissures_strings[4], inline=False)
            embed.set_footer(text=f"Last updated {datetime.now().strftime('%m/%d/%Y %H:%M')}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"🛑 An error occured! 🛑 \n```{traceback.format_exc()}```")

    # Checks what the current sortie is
    @commands.command(name='sortie', aliases=['st'], help='Gives information about today\'s sortie')
    async def sortie(self, ctx):
        try:
            request = requests.get('https://api.warframestat.us/pc/sortie')
            request.raise_for_status()
            response = request.json()

            stages = response['variants']

            embed = discord.Embed(title=f"Today's Sortie",
                                  colour=discord.Colour(0x4eb31c),
                                  description=f"Defeat {response['boss']}'s forces")
            
            embed.set_thumbnail(url=wfpics.get_boss_pic(response['boss']))
            embed.add_field(name=f"{stages[0]['node']} [Level 50-60]",
                            value= f"**{stages[0]['missionType']}** - {stages[0]['modifier']}",
                            inline=False)
            embed.add_field(name=f"{stages[1]['node']} [Level 65-80]",
                            value=f"**{stages[1]['missionType']}** - {stages[1]['modifier']}",
                            inline=False)
            embed.add_field(name=f"{stages[2]['node']} [Level 80-100]",
                            value=f"**{stages[2]['missionType']}** - {stages[2]['modifier']}",
                            inline=False)
            embed.set_footer(text=f"Last updated {datetime.now().strftime('%m/%d/%Y %H:%M')}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"🛑 An error occured! 🛑 \n```{traceback.format_exc()}```")

    # Checks information about invasions
    @commands.command(name='invasions', aliases=['inv'], help='Gives information about active invasions')
    async def invasions(self, ctx):
        try:
            request = requests.get('https://api.warframestat.us/pc/invasions')
            request.raise_for_status()
            response = request.json()

            # Separate out invasions to those vs a faction and those vs infested
            vs_faction_invasions = [inv for inv in response if not inv['vsInfestation'] and not inv['completed']]
            vs_infested_invasions = [inv for inv in response if inv['vsInfestation'] and not inv['completed']]

            faction_string = ""
            for inv in vs_faction_invasions:
                faction_string += f"[{int(inv['completion'])}%] **{inv['node']}** - {inv['desc']}\n{inv['attackerReward']['asString']} ({inv['attackingFaction']}) VS {inv['defenderReward']['asString']} ({inv['defendingFaction']})\n"
                if 'Infinity' not in inv['eta']:
                    faction_string += f"*{inv['eta']} remaining*\n"
                faction_string += "\n"

            infested_string = ""
            for inv in vs_infested_invasions:
                infested_string += f"[{int(inv['completion'])}%] **{inv['node']}** - {inv['desc']}\n{inv['defenderReward']['asString']}\n"
                if 'Infinity' not in inv['eta']:
                    infested_string += f"*{inv['eta']} remaining*\n"
                infested_string += "\n"

            embed = discord.Embed(title=f"Active Invasions",
                                  colour=discord.Colour(0x4eb31c))
            embed.add_field(name="Invasions", value=f"{faction_string}", inline=False)
            embed.add_field(name="Outbreaks", value=f"{infested_string}", inline=False)
            embed.set_footer(text=f"Last updated {datetime.now().strftime('%m/%d/%Y %H:%M')}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"🛑 An error occured! 🛑 \n```{traceback.format_exc()}```")

    # Checks information about Baro Ki-Teer's arrivals
    @commands.command(name='baro', aliases=['vt'], help='Check when Baro is coming and what he is selling')
    async def baro(self, ctx):
        try:
            request = requests.get('https://api.warframestat.us/pc/voidTrader')
            request.raise_for_status()
            response = request.json()

            # Handle the case where Baro isn't live yet
            if not response['active']:
                await ctx.send(f"Baro will be arriving at **{response['location']}** in {response['startString']}")
                return

            items_string = ""
            for item in response['inventory']:
                items_string += f"**{item['item']}** ({item['ducats']} Ducats\n"
            if not items_string:
                items_string = "*No items available*"

            embed = discord.Embed(title=f"This Week's Wares from the Void",
                                  colour=discord.Colour(0x4eb31c))
            embed.set_thumbnail(url="http://content.warframe.com/MobileExport/Lotus/Interface/Icons/Player/BaroKiteerAvatar.png")
            embed.add_field(name=f"*Departing in {response['endString']}*", 
                            value=items_string, inline=False)
            embed.set_footer(text=f"Last updated {datetime.now().strftime('%m/%d/%Y %H:%M')}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"🛑 An error occured! 🛑 \n```{traceback.format_exc()}```")

#sets up the client variable
def setup(client):
    client.add_cog(Worldstate(client))