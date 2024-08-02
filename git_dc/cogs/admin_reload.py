import discord
from discord.ext import commands

class admin_yeni(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(hidden=True)
    async def yenile(self, ctx, value:str) :
        
        dizin= "commands."
        
        try:
            if(ctx.author.guild_permissions.administrator):
              self.bot.reload_extension(dizin + value)
              await ctx.send(value+ " dosyası yenilendi")
            
            else:
                await ctx.send("bu komut için yetkiniz yok")       
        except ImportError as e:
            print(e)
            
            
async def setup(bot):
    await bot.add_cog(admin_yeni(bot))        