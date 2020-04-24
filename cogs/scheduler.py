import discord
from discord.ext import tasks, commands
import requests
import dateutil.parser
from datetime import date, datetime
from .worldstate import Worldstate # oh my gosh this is so jank

# Testing channel (2TestServPlsIgnore)
# DEFAULT_CHANNEL = 152673197756514304
# Production channel (SUMH Server)
DEFAULT_CHANNEL = 699321779172409344
POST_SORTIE_AT_TIME = "16:10"
POST_BARO_AT_TIME = "14"

class Scheduler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.worldstate = Worldstate(None)

    @tasks.loop(minutes=1)
    async def time_sortie(self):
        now = datetime.utcnow().strftime("%H:%M")
        if now == POST_SORTIE_AT_TIME:
            channel = self.client.get_channel(DEFAULT_CHANNEL)
            await self.worldstate.sortie(self.worldstate, ctx=channel)
        # await self.worldstate.sortie(self.worldstate, ctx=channel)
        # await self.worldstate.baro(self.worldstate, ctx=channel)

    @tasks.loop(minutes=60)
    async def time_baro(self):
        now = datetime.utcnow().strftime("%H")
        if now == POST_BARO_AT_TIME:
            if datetime.utcnow().date().weekday() == 4: # Friday
                request = requests.get('https://api.warframestat.us/pc/voidTrader')
                request.raise_for_status()
                response = request.json()
                if response['active']:
                    channel = self.client.get_channel(152673197756514304)
                    await self.worldstate.baro(self.worldstate, ctx=channel)

    # Checks current fissures and their time remaining
    @commands.command(name='debugscheduler', help='Check current system time', hidden=True)
    async def debugscheduler(self, ctx):
        try:
            await ctx.send(f"It is currently {datetime.utcnow().strftime('%m/%d/%Y %H:%M')}\nThis bot is scheduled to post sorties at {POST_SORTIE_AT_TIME} and Baro visits at {POST_BARO_AT_TIME} to channel {DEFAULT_CHANNEL}")
        except Exception as e:
            await ctx.send(f"🛑 An error occured! 🛑 \n```{traceback.format_exc()}```")


    #tells when it is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded cog: Command Scheduler (cogs/scheduler.py)')
        self.time_sortie.start()
        self.time_baro.start()

def setup(client):
    client.add_cog(Scheduler(client))