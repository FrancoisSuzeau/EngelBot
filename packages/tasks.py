import discord
from discord.ext import tasks, commands
import datetime
import json as js

class Tasks(commands.Cog):
    def __init__(self, bot, channels):
        self.bot = bot
        self.channels = channels
        self.auto_send.start()
        self.new_day = True
        self.load_config()
    
    def cog_unload(self):
        self.auto_send.cancel()

    def load_config(self):
        with open("materials/data/config.json") as file:
            config = js.load(file)['discord']
            self.task_hour = config['task_hour']

    def write_config(self):
        with open("materials/data/config.json", "r") as file:
            config = js.load(file)
        config['discord'] = {
            "task_hour":self.task_hour
        }
        json_object = js.dumps(config, indent=2)
        with open("materials/data/config.json", "w") as outfile:
            outfile.write(json_object)
        self.load_config()
        
    @tasks.loop(seconds=30.0)
    async def auto_send(self):
        now = datetime.datetime.now()
        if str(str(now.hour) + ":" + str(now.minute) + " am") == self.task_hour and self.new_day == True:
            for channel in self.channels:
                await channel.send("Let go for lunch at 12:00pm")
                self.new_day = False
        # else:
        #     print("not the time")
        if now.hour > 11:
            self.new_day = True

    @property
    def task_hour(self):
        return self._task_hour
    @task_hour.setter
    def task_hour(self, value):
        self._task_hour = value