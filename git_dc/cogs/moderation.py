import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def selamver(self, ctx):
        await ctx.send("merhaba")  # Kullanıcıya "merhaba" mesajı gönderir

async def setup(bot):
    await bot.add_cog(Moderation(bot))