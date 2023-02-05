import discord
from discord.ext import commands
import random
import pandas as pd 

class Member(commands.Cog):
    def __init__(self, bot, sentences, PICTURES_PATH, DATA_PATH):
        self.bot = bot
        self.sentences = sentences
        self.PICTURES_PATH = PICTURES_PATH
        self.DATA_PATH = DATA_PATH

    @commands.command(name='caca', help=": Responds with the highest dignity of his rank")
    async def poop_poop(self, ctx):
        poop_quotes = "POOOOOOOOOOP"
        await ctx.send(poop_quotes)

    @commands.command(name='ok', help=": Responds with a typical sentence")
    async def say_something(self, ctx):
        rand = random.randint(0, len(self.sentences))
        poop_quotes = self.sentences[rand]
        await ctx.send(poop_quotes)

    @commands.command(name='mephued', help=": Responds with a picture")
    async def show_something(self, ctx):
        rand = random.randint(1, 14)
        picure = discord.File(self.PICTURES_PATH + str(rand) + ".jpg")
        await ctx.send(file=picure)

    @commands.command(name='learn', help=": Add a new sentence in his BDD")
    async def learn_something(self, ctx, *, new_entry:str):
        if not(new_entry.endswith('.')) and not(new_entry.endswith('?')) and not(new_entry.endswith('!')):
            new_entry = new_entry + "."
        self.sentences[len(self.sentences)] = new_entry
        df = pd.DataFrame({0:self.sentences})
        df.to_csv(self.DATA_PATH + "backup.csv", header=False, index=False)
        await ctx.send("Vous voyez ? Grâce aux réseaux de neurone, j'ai appris quelque chose.")

    @commands.command(name='all', help=": Show all sentences")
    async def show_me_what_you_got(self, ctx):
        words = []
        for i in self.sentences:
            words.append(self.sentences[i])
        words = random.sample(words, len(words))
        for i in words:
            await ctx.send(i)