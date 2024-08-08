import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def bilgi(self, ctx):
     embed=discord.Embed(title="Bot Hakkında", color=0xc22e2e)
     embed.add_field(name="bot_version", value="0.11", inline=True)
     embed.add_field(name="bot_name", value="superbot", inline=True)
     embed.add_field(name="bot_creator", value="windness", inline=True)
     await ctx.send(embed=embed)    

async def setup(bot):
    await bot.add_cog(Moderation(bot))