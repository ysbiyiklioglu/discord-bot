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
    await load_extensions()
    print("uyandim") 

@Bot.command()
async def kick(ctx, member: discord.Member,*,sebep):
    await member.kick(reason=sebep)
    await ctx.send(f"**{member.mention}**, **{sebep}** sebebiyle sunucudan atıldı")
    

@Bot.command()
async def ban(ctx, member: discord.Member,*,sebep):
    await member.ban(reason=sebep)
    await ctx.send("üye sunucudan yasaklandı")




Bot.run("token")