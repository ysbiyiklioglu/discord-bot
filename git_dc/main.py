import os
import discord
from discord.ext import commands

Bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

initial_extensions = []
for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            initial_extensions.append("cogs." + filename[:-3])
async def load_extensions():
    for ext in initial_extensions:
        await Bot.load_extension(ext)
        
        
@Bot.event
async def on_ready(): #program ilk başladığında
    
    print("uyandim") 
    await load_extensions()
    
@Bot.event
async def on_member_join(member: discord.Member):
    Channel =discord.utils.get(member.guild.channels, name="yeni-gelenler")
    if Channel != None or Channel != 0:
        await Channel.send("Sunucumuza {} adında bir kullanıcı katıldı".format(member.mention))
    else:
        print("sunucudaki belirtilen kanal bulunamadı")
        
Bot.run("token")