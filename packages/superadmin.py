import discord
from discord.ext import commands

class SuperAdmin(commands.Cog):
    def __init__(self, bot, sentences, MyIn, MyT):
        self.bot = bot
        self.sentences = sentences
        self.MyIn = MyIn
        self.MyT = MyT

    @commands.command(name='task_hour', help=": Show his own task hour")
    @commands.has_role('SuperAdmin')
    async def show_task_hour(self, ctx):
        await ctx.send("Ma task hour est de : " + str(self.MyT.task_hour))

    @commands.command(name='edt_task_hour', help=": Change the hour of the task")
    @commands.has_role('SuperAdmin')
    async def edit_task_hour(self, ctx, *, value:str):
        self.MyT.task_hour = value
        self.MyT.write_config()
        await ctx.send("J'ai changé l'heure de mon message")

    @commands.command(name='create-channel', help=": Create a new channel")
    @commands.has_role('SuperAdmin')
    async def create_channel(self, ctx, channel_name='new channel tochange'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)
            
    @commands.command(name='all', help=": Show all sentences")
    @commands.has_role('SuperAdmin')
    async def show_me_what_you_got(self, ctx):
        for i in self.sentences:
            await ctx.send(self.sentences[i])
    
    @commands.command(name='tolerance', help=": Show his own tolerance")
    @commands.has_role('SuperAdmin')
    async def show_tolerance(self, ctx):
        await ctx.send("Ma tolerance est de : " + str(self.MyIn.tolerance))

    @commands.command(name='edt_tolerance', help=": Change his own tolerance")
    @commands.has_role('SuperAdmin')
    async def edit_tolerance(self, ctx, value:float):
        old = self.MyIn.tolerance
        self.MyIn.tolerance = float(value)
        self.MyIn.write_config()
        if old < self.MyIn.tolerance:
            await ctx.send("Attention, j'attends maintenant un certain niveau de language")
        elif old > self.MyIn.tolerance:
            if self.MyIn.tolerance <= 0.5:
                await ctx.send("Je n'ai plus besoin de réfléchir maintenant")
            else:
                await ctx.send("Je deviens un garagiste")
        elif old == self.MyIn.tolerance:
            await ctx.send("Je suis resté le même")

    @commands.command(name='epoch', help=": Show his own epoch")
    @commands.has_role('SuperAdmin')
    async def show_epoch(self, ctx):
        await ctx.send("Mon epoch est de : " + str(self.MyIn.epoch))

    @commands.command(name='edt_epoch', help=": Change his own epoch")
    @commands.has_role('SuperAdmin')
    async def edit_epoch(self, ctx, value:int):
        old = self.MyIn.epoch
        self.MyIn.epoch = int(value)
        self.MyIn.write_config()
        if old < self.MyIn.epoch:
            await ctx.send("Je vais mettre plus de temps pour m'entrainer maintenant")
        elif old > self.MyIn.epoch:
            if self.MyIn.epoch <= 200:
                await ctx.send("Mon modèle ne sera pas joli joli")
            else:
                await ctx.send("Je suis data scientist")
        elif old == self.MyIn.epoch:
            await ctx.send("Je suis resté le même")

    @commands.command(name='train', help=": Retrain his own model")
    @commands.has_role('SuperAdmin')
    async def retrain_model(self, ctx):
        self.MyIn.clean_cache()
        self.MyIn.load_data()
        self.MyIn.train_model()
        await ctx.send("C'est bon, j'ai réentrainé mon model")

    @commands.command(name='chat', help=": Chat with the user")
    @commands.has_role('SuperAdmin')
    async def on_chat(self, ctx, *, content):
        if len(content) <= 1:
            await ctx.send("Vous m'avez appelé ?")
        else:
            await ctx.send(self.MyIn.chat(content))

    @commands.command(name='shutdown', help=': Goes offline')
    @commands.has_role('SuperAdmin')
    async def shutdown(self, ctx):
        await ctx.send("On va s'arreter la pour aujourd'hui")
        await self.bot.close()